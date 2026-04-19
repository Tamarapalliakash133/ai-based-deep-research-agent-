from flask import Flask, render_template, request
import asyncio
import os
from graph import graph_build, config

app = Flask(__name__)

def run_async(coro):
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    return loop.run_until_complete(coro)

@app.route("/", methods=["GET", "POST"])
def home():
    result = None

    if request.method == "POST":
        topic = request.form.get("topic")

        if not topic:
            return render_template("index.html", result="Please enter a topic")

        deep_research = run_async(
            graph_build.ainvoke(
                {"topic": topic},
                config=config
            )
        )

        result = deep_research.get("final_report", "No result generated")

    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000))
    )
