from flask import Flask, jsonify, request, render_template
import requests

app = Flask(__name__)


@app.route('/api/citations', methods=['GET'])
def get_citations():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))

    data = fetch_data(page, per_page)
    citations = identify_citations(data)

    return jsonify(citations)


def fetch_data(page, per_page):
    api_url = f"https://devapi.beyondchats.com/api/get_message_with_sources?page={page}&per_page={per_page}"
    response = requests.get(api_url)
    response.raise_for_status()
    return response.json()


def identify_citations(data):
    citations = []
    if "data" in data:
        for item in data["data"].get("data", []):
            for source in item.get("source", []):
                link = source.get("link")
                if link:
                    citations.append({"id": source["id"], "link": link})
    print(citations)
    return citations


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
