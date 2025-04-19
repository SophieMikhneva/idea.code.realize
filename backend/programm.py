from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from uuid import uuid4
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///presentations.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Модели базы данных
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    role = db.Column(db.String(20), nullable=False)
    group_id = db.Column(db.String(20))
    department = db.Column(db.String(100))


class Group(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(100), nullable=False)


class Subject(db.Model):
    __tablename__ = 'subjects'
    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    teacher_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)


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


# Создаем базу данных при первом запуске
with app.app_context():
    db.create_all()
    # Добавляем тестовых пользователей, если их нет
    if not User.query.first():
        db.session.add_all([
            User(
                id=str(uuid4()),
                name="Иван Петров",
                email="ivan@university.ru",
                role="student",
                group_id="CS-101",
                department=None
            ),
            User(
                id=str(uuid4()),
                name="Анна Сидорова",
                email="anna@university.ru",
                role="teacher",
                group_id=None,
                department="Информатика"
            )
        ])
        db.session.commit()


# Главная страница
@app.route('/')
def index():
    return render_template('index.html')


# Все презентации
@app.route('/api/presentations', methods=['GET'])
def get_presentations():
    presentations = Presentation.query.all()
    result = []
    for pres in presentations:
        # Получаем связанные данные
        author = User.query.get(pres.author_id)
        comments = Comment.query.filter_by(presentation_id=pres.id).all()
        supplements = Supplement.query.filter_by(presentation_id=pres.id).all()

        result.append({
            "id": pres.id,
            "title": pres.title,
            "description": pres.description,
            "authorId": pres.author_id,
            "authorName": author.name if author else None,
            "subjectId": pres.subject_id,
            "groupId": pres.group_id,
            "uploadDate": pres.upload_date.strftime('%Y-%m-%d'),
            "lastModified": pres.last_modified.strftime('%Y-%m-%d'),
            "file": {
                "name": pres.file_name,
                "type": pres.file_type
            },
            "rating": float(pres.rating) if pres.rating else 0,
            "downloads": pres.downloads,
            "comments": [{
                "id": c.id,
                "userId": c.user_id,
                "text": c.text,
                "date": c.date.strftime('%Y-%m-%d')
            } for c in comments],
            "supplements": [{
                "id": s.id,
                "authorId": s.author_id,
                "url": s.url,
                "date": s.date.strftime('%Y-%m-%d'),
                "description": s.description
            } for s in supplements]
        })
    return jsonify(result)


# Добавить новую презентацию
@app.route('/api/presentations', methods=['POST'])
def add_presentation():
    req = request.json
    today = datetime.today()

    new_pres = Presentation(
        id=str(uuid4()),
        title=req["title"],
        description=req.get("description", ""),
        author_id=req["authorId"],
        subject_id=req.get("subjectId"),
        group_id=req.get("groupId"),
        upload_date=today,
        last_modified=today,
        file_name=req["fileName"],
        file_type=req.get("fileType", "presentation"),
        rating=0,
        downloads=0
    )

    db.session.add(new_pres)
    db.session.commit()

    # Возвращаем данные в том же формате, что и в оригинальной версии
    return jsonify({
        "id": new_pres.id,
        "title": new_pres.title,
        "description": new_pres.description,
        "authorId": new_pres.author_id,
        "subjectId": new_pres.subject_id,
        "groupId": new_pres.group_id,
        "uploadDate": new_pres.upload_date.strftime('%Y-%m-%d'),
        "lastModified": new_pres.last_modified.strftime('%Y-%m-%d'),
        "file": {
            "name": new_pres.file_name,
            "type": new_pres.file_type
        },
        "rating": 0,
        "downloads": 0,
        "comments": [],
        "supplements": []
    }), 201


# Оценить презентацию
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


# Добавить комментарий
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

    # Обновленный список комментариев
    comments = Comment.query.filter_by(presentation_id=presentation_id).all()
    return jsonify([{
        "id": c.id,
        "userId": c.user_id,
        "text": c.text,
        "date": c.date.strftime('%Y-%m-%d')
    } for c in comments])


# Добавить доп материал
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

    # Возвращаем обновленный список допматериалов
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
    return render_template('presentations.html')

@app.route('/upload')
def upload_presentation():
    return render_template('upload.html')


if __name__ == '__main__':
    app.run(debug=True)
