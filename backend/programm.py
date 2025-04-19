from flask import Flask, request, jsonify, render_template
import os
import json
from uuid import uuid4
from datetime import datetime

app = Flask(__name__)

DATA_FILE = os.path.join('data', 'database.json')

if not os.path.exists('data'):
    os.makedirs('data')
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump({"users": [], "groups": [], "subjects": [], "presentations": []}, f)

def load_data():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# Главная страница
@app.route('/')
def index():
    return render_template('index.html')  # Фронтенд

# Все презентации
@app.route('/api/presentations', methods=['GET'])
def get_presentations():
    data = load_data()
    return jsonify(data['presentations'])

# Добавить новую презентацию
@app.route('/api/presentations', methods=['POST'])
def add_presentation():
    req = request.json
    data = load_data()
    today = datetime.today().strftime('%Y-%m-%d')

    new_pres = {
        "id": str(uuid4()),
        "title": req["title"],
        "description": req.get("description", ""),
        "authorId": req["authorId"],
        "subjectId": req.get("subjectId"),
        "groupId": req.get("groupId"),
        "uploadDate": today,
        "lastModified": today,
        "file": {
            "name": req["fileName"],
            "type": req.get("fileType", "presentation")
        },
        "rating": 0,
        "downloads": 0,
        "tags": req.get("tags", []),
        "comments": [],
        "supplements": []
    }

    data["presentations"].append(new_pres)
    save_data(data)
    return jsonify(new_pres), 201

# Оценить презентацию
@app.route('/api/presentations/<presentation_id>/rate', methods=['POST'])
def rate_presentation(presentation_id):
    delta = request.json.get("delta", 1)
    data = load_data()

    for pres in data["presentations"]:
        if pres["id"] == presentation_id:
            pres["rating"] += delta
            save_data(data)
            return jsonify(pres)
    return jsonify({"error": "Presentation not found"}), 404

# Добавить комментарий
@app.route('/api/presentations/<presentation_id>/comment', methods=['POST'])
def add_comment(presentation_id):
    req = request.json
    data = load_data()
    today = datetime.today().strftime('%Y-%m-%d')

    for pres in data["presentations"]:
        if pres["id"] == presentation_id:
            pres["comments"].append({
                "id": str(uuid4()),
                "userId": req["userId"],
                "text": req["text"],
                "date": today
            })
            save_data(data)
            return jsonify(pres)
    return jsonify({"error": "Presentation not found"}), 404

# Добавить доп. материал
@app.route('/api/presentations/<presentation_id>/supplement', methods=['POST'])
def add_supplement(presentation_id):
    req = request.json
    today = datetime.today().strftime('%Y-%m-%d')
    data = load_data()

    for pres in data["presentations"]:
        if pres["id"] == presentation_id:
            pres["supplements"].append({
                "id": str(uuid4()),
                "authorId": req["authorId"],
                "url": req["url"],
                "date": today,
                "description": req.get("description", "")
            })
            save_data(data)
            return jsonify(pres)
    return jsonify({"error": "Presentation not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
