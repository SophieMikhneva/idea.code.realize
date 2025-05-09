from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
from uuid import uuid4

app = Flask(__name__, static_folder=None)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///presentations.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Модели БД
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    role = db.Column(db.String(20), nullable=False, default='student')
    group_id = db.Column(db.String(20), db.ForeignKey('groups.id'))
    department = db.Column(db.String(100))

    __table_args__ = (
        db.CheckConstraint("role = 'student'", name='chk_role'),
    )


class Group(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(100), nullable=False)


class Subject(db.Model):
    __tablename__ = 'subjects'
    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(100), nullable=False)


# Связующая таблица групп и предметов
class GroupSubject(db.Model):
    __tablename__ = 'group_subjects'
    group_id = db.Column(db.String(20), db.ForeignKey('groups.id', ondelete='CASCADE'), primary_key=True)
    subject_id = db.Column(db.String(36), db.ForeignKey('subjects.id', ondelete='CASCADE'), primary_key=True)


class Presentation(db.Model):
    __tablename__ = 'presentations'
    id = db.Column(db.String(36), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    author_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    subject_id = db.Column(db.String(36), db.ForeignKey('subjects.id'), nullable=False)
    group_id = db.Column(db.String(20), db.ForeignKey('groups.id'))
    upload_date = db.Column(db.Date, nullable=False)
    last_modified = db.Column(db.DateTime, nullable=False)
    file_name = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(50), default='presentation')
    rating = db.Column(db.Numeric(3, 1), default=0)
    downloads = db.Column(db.Integer, default=0)


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.String(36), primary_key=True)
    presentation_id = db.Column(db.String(36), db.ForeignKey('presentations.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.Date, nullable=False)


class Supplement(db.Model):
    __tablename__ = 'supplements'
    id = db.Column(db.String(36), primary_key=True)
    presentation_id = db.Column(db.String(36), db.ForeignKey('presentations.id'), nullable=False)
    author_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    url = db.Column(db.Text, nullable=False)
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text)

@app.route("/")
def index():
    return render_template("index.html", api_url="/api/presentations")

@app.route('/api/subjects', methods=['GET'])
def get_subjects():
    subjects = Subject.query.all()
    result = [{"id": s.id, "name": s.name} for s in subjects]
    return jsonify(result)


@app.route('/api/presentations', methods=['GET'])
def get_presentations():
    title = request.args.get('title', '').strip()
    q = Presentation.query
    if title:
        q = q.filter(Presentation.title.ilike(f"%{title}%"))
    presentations = q.all()
    result = []
    for p in presentations:
        result.append({
            "id": p.id,
            "title": p.title,
            "description": p.description,
            "subjectId": p.subject_id,
            "uploadDate": p.upload_date.strftime('%Y-%m-%d'),
            "file": {
                "name": p.file_name,
                "type": p.file_type
            },
            "rating": float(p.rating or 0),
            "downloads": p.downloads
        })

    return jsonify(result)


# Эндпоинт для поиска предметов
@app.route('/api/subjects/search', methods=['GET'])
def search_subjects():
    query = request.args.get('query', '').strip()

    # Базовый запрос
    q = Subject.query

    # Фильтр по названию предмета (если передан)
    if query:
        q = q.filter(Subject.name.ilike(f"%{query}%"))

    # Получаем результаты
    subjects = q.all()

    # Формируем ответ
    result = [{
        "id": s.id,
        "name": s.name
    } for s in subjects]

    return jsonify(result)

@app.route('/api/presentations', methods=['POST'])
def add_presentation():
    data = request.json
    now = datetime.now()

    new_id = str(uuid4())
    p = Presentation(
        id=new_id,
        title=data['title'],
        description=data.get('description', ''),
        author_id=data['authorId'],
        subject_id=data.get('subjectId'),
        group_id=data.get('groupId'),
        upload_date=now.date(),
        last_modified=now,
        file_name=data['fileName'],
        file_type=data.get('fileType', 'presentation')
    )
    db.session.add(p)
    db.session.commit()
    return jsonify({
        "id": new_id,
        "title": p.title,
        "authorId": p.author_id,
        "file": {
            "name": p.file_name,
            "type": p.file_type
        },
        "uploadDate": str(p.upload_date),
        "lastModified": str(p.last_modified.date()),
        "rating": 0,
        "downloads": 0,
        "comments": [],
        "supplements": []
    }), 201

@app.route('/api/presentations/<presentation_id>/rate', methods=['POST'])
def rate_presentation(presentation_id):
    delta = request.json.get("delta", 1)
    pres = Presentation.query.get(presentation_id)

    if not pres:
        return jsonify({"error": "Presentation not found"}), 404

    pres.rating += delta
    db.session.commit()

    return jsonify({
        "id": pres.id,
        "rating": float(pres.rating)
    })

@app.route('/api/presentations/<presentation_id>/comment', methods=['POST'])
def add_comment(presentation_id):
    req = request.json
    today = datetime.today()

    new_comment = Comment(
        id=str(uuid4()),
        presentation_id=presentation_id,
        user_id=req["userId"],
        text=req["text"],
        date=today
    )

    db.session.add(new_comment)
    db.session.commit()

    comments = Comment.query.filter_by(presentation_id=presentation_id).all()
    return jsonify([{
        "id": c.id,
        "userId": c.user_id,
        "text": c.text,
        "date": c.date.strftime('%Y-%m-%d')
    } for c in comments])

@app.route('/api/presentations/<presentation_id>/supplement', methods=['POST'])
def add_supplement(presentation_id):
    req = request.json
    today = datetime.today()

    new_supplement = Supplement(
        id=str(uuid4()),
        presentation_id=presentation_id,
        author_id=req["authorId"],
        url=req["url"],
        date=today,
        description=req.get("description", "")
    )

    db.session.add(new_supplement)
    db.session.commit()

    supplements = Supplement.query.filter_by(presentation_id=presentation_id).all()
    return jsonify([{
        "id": s.id,
        "authorId": s.author_id,
        "url": s.url,
        "date": s.date.strftime('%Y-%m-%d'),
        "description": s.description
    } for s in supplements])

@app.route('/presentations')
def show_presentations():
    title = request.args.get('title')
    author = request.args.get('author')
    subject = request.args.get('subject')
    group = request.args.get('group')

    api_url = "/api/presentations?"
    if title: api_url += f"title={title}&"
    if author: api_url += f"author={author}&"
    if subject: api_url += f"subject={subject}&"
    if group: api_url += f"group={group}&"
    api_url = api_url.rstrip("&")

    return render_template('presentations.html', api_url=api_url)

@app.route('/upload')
def upload_presentation():
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
