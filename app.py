from flask import Flask, render_template, request
import os
import matplotlib.pyplot as plt
import networkx as nx
from sklearn.cluster import AgglomerativeClustering
from plagiarism import pairwise_similarity

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def cluster_programs(similarity_matrix, threshold=0.8):
    distance = 1 - similarity_matrix

    clustering = AgglomerativeClustering(
        metric="precomputed",
        linkage="average",
        distance_threshold=1 - threshold,
        n_clusters=None
    )

    labels = clustering.fit_predict(distance)
    return labels


def generate_graph(files, matrix, threshold=0.8):
    G = nx.Graph()

    for f in files:
        G.add_node(f)

    for i in range(len(files)):
        for j in range(i + 1, len(files)):
            if matrix[i][j] >= threshold:
                G.add_edge(files[i], files[j])

    pos = nx.spring_layout(G)
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True)
    plt.savefig("static/graph.png")
    plt.close()


@app.route("/", methods=["GET", "POST"])
def index():
    results = None
    clusters = None
    error = None  # NEW

    if request.method == "POST":
        uploaded_files = request.files.getlist("files")

        # 🚨 Check if user selected files
        if not uploaded_files or uploaded_files[0].filename == "":
            error = "Please select Python files before clicking Analyze."
            return render_template(
                "index.html",
                results=None,
                clusters=None,
                error=error
            )

        programs = {}

        for file in uploaded_files:
            if file.filename.endswith(".py"):
                try:
                    code = file.read().decode("utf-8")
                    if code.strip():
                        programs[file.filename] = code
                except:
                    continue

        # Second validation (need at least 2 programs)
        if len(programs) < 2:
            error = "Upload at least 2 valid Python programs."
            return render_template(
                "index.html",
                results=None,
                clusters=None,
                error=error
            )

        files, matrix = pairwise_similarity(programs)
        labels = cluster_programs(matrix)

        generate_graph(files, matrix)

        results = []
        for i in range(len(files)):
            for j in range(i + 1, len(files)):
                results.append(
                    (files[i], files[j], round(matrix[i][j], 3))
                )

        clusters = list(zip(files, labels))

    return render_template(
        "index.html",
        results=results,
        clusters=clusters,
        error=error
    )


if __name__ == "__main__":
    app.run(debug=True)
