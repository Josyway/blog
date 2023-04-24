from flask import render_template, redirect, url_for, flash, request
from blogpy import app, database, bcrypt
from blogpy.forms import FormLogin, FormCriarConta, FormEditarPerfil, FormCriarPost, FormEditarPost
from blogpy.models import Usuario, Post
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os
from PIL import Image

@app.route('/')
def home():
    posts = Post.query.order_by(Post.id.desc())
    return render_template('home.html', posts=posts)

@app.route('/contato')
def contato():
    return render_template('contato.html')

@app.route('/usuarios')
@login_required
def usuarios():
    lista_usuarios = Usuario.query.all()
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    if form_login.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=form_login.lembrar_dados.data)
            flash(f"Login realizado com sucesso para o e-mail {form_login.email.data}", 'alert-success')
            par_next = request.args.get('next')
            if par_next:
                return redirect(par_next)
            else:
                return redirect(url_for('home'))
        else:
            flash("E-mail ou Senha Incorreto", 'alert-danger')
    return render_template('login.html', form_login=form_login)

@app.route('/criarconta', methods=['GET', 'POST'])
def criarconta():
    form_criarconta = FormCriarConta()
    if form_criarconta.validate_on_submit():
        senha_cript = bcrypt.generate_password_hash(form_criarconta.senha.data)
        usuario = Usuario(username=form_criarconta.username.data, email=form_criarconta.email.data, senha=senha_cript)
        database.session.add(usuario)
        database.session.commit()
        flash(f"Conta criada com sucesso para o e-mail {form_criarconta.email.data}", 'alert-success')
        return redirect(url_for('home'))
    return render_template('criarconta.html', form_criarconta=form_criarconta)

@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash(f"Logout Feito com Sucesso", 'alert-success')
    return redirect(url_for('home'))

@app.route('/perfil')
@login_required
def perfil():
    foto_perfil = url_for('static', filename=f'fotos_perfil/{current_user.foto_perfil}')
    return render_template('perfil.html', foto_perfil=foto_perfil)

@app.route('/post/criar', methods=['GET', 'POST'])
@login_required
def criar_post():
    form_criarpost = FormCriarPost()
    if form_criarpost.validate_on_submit():
        post = Post(titulo=form_criarpost.titulo.data, corpo=form_criarpost.corpo.data, autor=current_user)
        database.session.add(post)
        database.session.commit()
        flash('Post Criado com Sucesso!', 'alert-success')
        return redirect(url_for('home'))
    return render_template('criarpost.html', form_criarpost=form_criarpost)

def salvar_imagem(imagem):
    codigo = secrets.token_hex(8)
    nome, extensao = os.path.splitext(imagem.filename)
    nome_arquivo = nome + codigo + extensao
    caminho_salvar = os.path.join(app.root_path, 'static/fotos_perfil', nome_arquivo )
    tamanho = (400, 400)
    img_reduzida =  Image.open(imagem)
    img_reduzida.thumbnail(tamanho)
    img_reduzida.save(caminho_salvar)
    return nome_arquivo

def atualizar_cursos(form_editarperfil):
    lista_cursos = []
    for campo in form_editarperfil:
        if "curso_" in campo.name:
            if campo.data:
                lista_cursos.append(campo.label.text)
    return ';'.join(lista_cursos)

@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form_editarperfil = FormEditarPerfil()
    if form_editarperfil.validate_on_submit():
        current_user.username = form_editarperfil.username.data
        if form_editarperfil.foto_perfil.data:
            nome_imagem = salvar_imagem(form_editarperfil.foto_perfil.data)
            current_user.foto_perfil = nome_imagem
        current_user.cursos = atualizar_cursos(form_editarperfil)

        database.session.commit()
        flash(f"Perfil atualizado com Sucesso!", 'alert-success')
        return redirect(url_for('perfil'))
    foto_perfil = url_for('static', filename=f'fotos_perfil/{current_user.foto_perfil}')
    return render_template('editarperfil.html', foto_perfil=foto_perfil, form_editarperfil=form_editarperfil)

@app.route('/post/<post_id>')
@login_required
def exibir_post(post_id):
    post = Post.query.get(post_id)
    return render_template('post.html', post=post)

@app.route('/post/editar/<post_id>', methods=['GET', 'POST'])
@login_required
def editar_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        form_editarpost = FormEditarPost()
        if request.method == 'GET':
            form_editarpost.titulo.data = post.titulo
            form_editarpost.corpo.data = post.corpo
        elif form_editarpost.validate_on_submit():
            post.titulo = form_editarpost.titulo.data
            post.corpo = form_editarpost.corpo.data
            database.session.commit()
            flash('Post Atualizado com Sucesso', 'alert-success')
            return redirect(url_for('home'))
    else:
        form_editarpost = None
    return render_template('editarpost.html', post=post, form_editarpost=form_editarpost)

@app.route('/post/<post_id>/excluir', methods=['GET', 'POST'])
@login_required
def excluir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        database.session.delete(post)
        database.session.commit()
        flash('Post excluido com Sucesso!', 'alert-danger')
        return redirect(url_for('home'))
    else:
        flash('Você não pode exclir esse Post', 'alert-danger')
        return redirect(url_for('home'))
