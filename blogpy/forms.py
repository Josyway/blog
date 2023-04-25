from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, fields, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from blogpy.models import Usuario
from flask_login import current_user


class FormCriarConta(FlaskForm):
    username = StringField('Nome', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    confirmar_senha = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('senha')])
    botao_submit_criarconta = SubmitField(' Criar Conta')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('E-mail já cadastrado.')

class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    lembrar_dados = BooleanField('Lembrar Dados de Acesso')
    botao_submit_login = SubmitField('Entrar')

class FormEditarPerfil(FlaskForm):
    username = StringField('Nome', validators=[DataRequired()])
    foto_perfil = FileField('Atualizar Foto de Perfil', validators=[FileAllowed(['jpg', 'png'])])
    curso_pyton = BooleanField('Python')
    curso_sql = BooleanField('SQL')
    curso_vba = BooleanField('VBA')
    curso_excel = BooleanField('Excel')
    curso_powerpoint = BooleanField('PowerPoint')
    curso_power_bi = BooleanField('Power BI')
    curso_power_apps = BooleanField('Power apps')
    curso_lonkdin = BooleanField('Linkdin')
    curso_processo_seletivo = BooleanField('Processo Seletivo')
    botao_submit_editarperfil = SubmitField('Salvar Perfil')

    def validate_usuario(self, username):
        if current_user.username != username.data:
            usuario = Usuario.query.filter_by(email=username.data).first()
            if usuario:
                raise ValidationError('Já exixte um usuário com esse perfil!')

class FormCriarPost(FlaskForm):
    titulo = StringField('Titulo do Post', validators=[DataRequired(), Length(2, 140)])
    corpo = TextAreaField('Escreva seu Post', validators=[DataRequired()])
    botao_submit_criarpost = SubmitField('Criar Post')


class FormEditarPost(FlaskForm):
    titulo = StringField('Titulo do Post', validators=[DataRequired(), Length(2, 140)])
    corpo = TextAreaField('Escreva seu Post', validators=[DataRequired()])
    botao_submit_editarpost = SubmitField('Salvar Editar')
    otao_submit_excluirpost = SubmitField('Excluir Poster')
