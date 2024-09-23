from flask import jsonify, request, session, redirect
from app import app, db
from models import Usuario, PostFeed, WarningsForFeed, Coordinator


@app.route('/register/quick', methods=['POST'])
def register_quick():
    data = request.json
    usuario = Usuario(
        usuario=data.get('usuario'),
        idade=data.get('idade'),
        interesse=data.get('interesse'),
        email=data.get('email'),
        permissao=data.get('permissao')
    )
    db.session.add(usuario)
    db.session.commit()
    return jsonify({'message': 'Usuario registrado com sucesso - Registro rapido feito'}), 201


# Cadastro completo
@app.route('/register/full', methods=['POST'])
def register_full():
    data = request.json
    usuario = Usuario(
        matricula=data.get('matricula'),
        email=data.get('email'),
        nome=data.get('nome'),
        cpf=data.get('cpf'),
        senha=data.get('senha'),
        idade=data.get('idade')
    )

    try:
        db.session.add(usuario)
        db.session.commit()
        return jsonify({'message': 'Usuário registrado com sucesso - Registro completo feito'}), 201

    except Exception as e:
        # Se ocorrer algum erro durante a inserção no banco de dados
        db.session.rollback()
        return jsonify({'message': f'Erro ao registrar usuário: {str(e)}'}), 500

# Login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    usuario = Usuario.query.filter_by(matricula=data.get('matricula'), cpf=data.get('cpf')).first()
    if usuario and usuario.senha == data.get('senha'):
        return jsonify({'message': 'Login bem-sucedido'}), 200
    else:
        return jsonify({'message': 'Login inválidas'}), 401


# Criação de post
@app.route('/posts', methods=['POST'])
def create_post():
    data = request.json
    post = PostFeed(
        img_id=data.get('img_id'),
        description=data.get('description'),
        likes=data.get('likes', 0),
        comments=data.get('comments'),
        category=data.get('category'),
        course=data.get('course'),
        status=data.get('status', False),
        user_id=data.get('user_id')
    )
    db.session.add(post)
    db.session.commit()
    return jsonify({'message': 'Postagem criada com sucesso'}), 201


# Deletar post
@app.route('/posts/<int:postfeed_id>', methods=['DELETE'])
def delete_post(postfeed_id):
    post = PostFeed.query.get(postfeed_id)
    if post:
        db.session.delete(post)
        db.session.commit()
        return jsonify({'message': 'Post deletado com sucesso'}), 200
    else:
        return jsonify({'message': 'Post não encontrado'}), 404


# Aprovar post
@app.route('/posts/approve/<int:postfeed_id>', methods=['PUT'])
def approve_post(postfeed_id):
    post = PostFeed.query.get(postfeed_id)
    if post:
        post.status = 1
        db.session.commit()
        return jsonify({'message': 'Post aprovado com sucesso'}), 200
    else:
        return jsonify({'message': 'Post não encontrado'}), 404


# Obter posts
@app.route('/posts', methods=['GET'])
def get_posts():
    posts = PostFeed.query.filter_by(status=1).all()
    return jsonify([{
        'postfeed_id': post.postfeed_id,
        'img_id': post.img_id,
        'description': post.description,
        'likes': post.likes,
        'comments': post.comments,
        'category': post.category,
        'course': post.course,
        'status': post.status,
        'user_id': post.user_id
    } for post in posts]), 200


@app.route('/posts/valida', methods=['GET'])
def get_posts_valida():
    posts = PostFeed.query.filter_by(status=0).all()
    return jsonify([{
        'postfeed_id': post.postfeed_id,
        'img_id': post.img_id,
        'description': post.description,
        'likes': post.likes,
        'comments': post.comments,
        'category': post.category,
        'course': post.course,
        'status': post.status,
        'user_id': post.user_id
    } for post in posts]), 200


# Cadastro de aviso
@app.route('/warnings', methods=['POST'])
def create_warning():
    data = request.json
    warning = WarningsForFeed(
        priority=data.get('priority'),
        content=data.get('content'),
        img_id=data.get('img_id'),
        coordinator_id=data.get('coordinator_id')
    )
    db.session.add(warning)
    db.session.commit()
    return jsonify({'message': 'Aviso criado com sucesso'}), 201


# Obter avisos
@app.route('/warnings', methods=['GET'])
def get_warnings():
    warnings = WarningsForFeed.query.all()
    return jsonify([{
        'warnings_id': warning.warnings_id,
        'priority': warning.priority,
        'content': warning.content,
        'img_id': warning.img_id,
        'coordinator_id': warning.coordinator_id
    } for warning in warnings]), 200


@app.route('/posts/<int:postfeed_id>', methods=['GET'])
def get_post(postfeed_id):
    post = PostFeed.query.get(postfeed_id)
    if post:
        return jsonify({
            'postfeed_id': post.postfeed_id,
            'img_id': post.img_id,
            'description': post.description,
            'likes': post.likes,
            'comments': post.comments,
            'category': post.category,
            'course': post.course,
            'status': post.status,
            'user_id': post.user_id
        }), 200
    else:
        return jsonify({'message': 'Post não encontrado'}), 404


@app.route('/posts/<int:postfeed_id>', methods=['PUT'])
def update_post(postfeed_id):
    data = request.json
    post = PostFeed.query.get(postfeed_id)
    if post:
        post.img_id = data.get('img_id', post.img_id)
        post.description = data.get('description', post.description)
        post.likes = data.get('likes', post.likes)
        post.comments = data.get('comments', post.comments)
        post.category = data.get('category', post.category)
        post.course = data.get('course', post.course)
        post.status = data.get('status', post.status)
        db.session.commit()
        return jsonify({'message': 'Post atualizado com sucesso'}), 200
    else:
        return jsonify({'message': 'Post não encontrado'}), 404


@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    usuario = Usuario.query.get(user_id)
    if usuario:
        usuario.usuario = data.get('usuario', usuario.usuario)
        usuario.idade = data.get('idade', usuario.idade)
        usuario.interesse = data.get('interesse', usuario.interesse)
        usuario.email = data.get('email', usuario.email)
        usuario.permissao = data.get('permissao', usuario.permissao)
        usuario.matricula = data.get('matricula', usuario.matricula)
        usuario.nome = data.get('nome', usuario.nome)
        usuario.cpf = data.get('cpf', usuario.cpf)
        usuario.senha = data.get('senha', usuario.senha)
        db.session.commit()
        return jsonify({'message': 'Usuário atualizado com sucesso'}), 200
    else:
        return jsonify({'message': 'Usuário não encontrado'}), 404


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    usuario = Usuario.query.get(user_id)
    if usuario:
        db.session.delete(usuario)
        db.session.commit()
        return jsonify({'message': 'Usuário excluído com sucesso'}), 200
    else:
        return jsonify({'message': 'Usuário não encontrado'}), 404


@app.route('/login/coordinator', methods=['POST'])
def login_coordinator():
    data = request.json
    cpf = data.get('cpf')
    password = data.get('password')

    coordinator = Coordinator.query.filter_by(cpf=cpf, password=password).first()


    if coordinator:
        return jsonify({
            'message': 'Login de coordenador bem-sucedido',
            'coordinator_id': coordinator.coordinator_id,
            'nome': coordinator.name
        }), 200
    else:
        return jsonify({'message': 'CPF ou senha inválidos para coordenador'}), 404
