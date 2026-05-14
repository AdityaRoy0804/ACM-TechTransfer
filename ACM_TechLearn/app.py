from flask import Flask, render_template, request, jsonify
import http.client
import json

app = Flask(__name__)

SERPER_API_KEY = "8206d4b06660132fd0c07a44697deaae59ac181a"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/study")
def study():
    return render_template("study.html")

@app.route("/coding")
def coding():
    return render_template("coding.html")

@app.route("/search")
def search():

    topic = request.args.get("topic")

    conn = http.client.HTTPSConnection("google.serper.dev")

    payload = json.dumps({
        "q": topic,
        "gl": "in"
    })

    headers = {
        'X-API-KEY': SERPER_API_KEY,
        'Content-Type': 'application/json'
    }

    conn.request("POST", "/search", payload, headers)

    res = conn.getresponse()
    data = res.read()

    result = json.loads(data.decode("utf-8"))

    description = ""
    link = ""
    video = ""

    if "organic" in result and len(result["organic"]) > 0:
        description = result["organic"][0]["snippet"]
        link = result["organic"][0]["link"]

    if "videos" in result and len(result["videos"]) > 0:
        video = result["videos"][0]["link"]

    return jsonify({
        "description": description,
        "article": link,
        "video": video
    })

if __name__ == "__main__":
    app.run(debug=True)