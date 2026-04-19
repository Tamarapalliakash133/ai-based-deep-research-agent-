from flask import Flask, render_template, request
import asyncio
import os
from graph import graph_build, config

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    result = None

    if request.method == "POST":
        topic = request.form.get("topic")

        deep_research = asyncio.run(
            graph_build.ainvoke(
                {"topic": topic},
                config=config
            )
        )

        result = deep_research.get("final_report", "No result generated")

    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(debug=True,host = "0.0.0.0", port = int(os.environ.get("PORT",10000)))
