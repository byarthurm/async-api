from app import db


class Usuario(db.Model):
    __tablename__ = 'usuario'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer)
    interesse = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True, nullable=False)
    permissao = db.Column(db.Integer, default=0)
    matricula = db.Column(db.String(100), unique=True)
    nome = db.Column(db.String(100))
    cpf = db.Column(db.String(14), unique=True)
    senha = db.Column(db.String(100))


class PostFeed(db.Model):
    __tablename__ = 'Post_Feed'

    postfeed_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    img_id = db.Column(db.String(255))
    description = db.Column(db.Text)
    likes = db.Column(db.Integer, default=0)
    comments = db.Column(db.Text)
    category = db.Column(db.String(100))
    course = db.Column(db.String(100))
    titulo = db.Column(db.String(255))
    status = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('usuario.user_id'), nullable=False)  # Corrigido


class WarningsForFeed(db.Model):
    __tablename__ = 'Warnings_For_Feed'

    warnings_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    priority = db.Column(db.Integer)
    content = db.Column(db.Text)
    img_id = db.Column(db.Integer)
    coordinator_id = db.Column(db.Integer, db.ForeignKey('Coordinator.coordinator_id'))
    coordinator = db.relationship('Coordinator', backref=db.backref('warnings', lazy=True))


class Coordinator(db.Model):
    __tablename__ = 'Coordinator'

    coordinator_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
