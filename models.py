from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Livro(db.Model):
    _tablename_ = 'livros'

    id = db.Column(db.Integer, primary_key = True,
                   autoincrement = True, nullable=False, unique=True)
    titulo = db.Column(db.String,  nullable = False)
    autor = db.Column(db.String,  nullable = False)
    ano = db.Column(db.String,  nullable = False)
    genero = db.Column(db.String,  nullable = False)
    editora = db.Column(db.String,  nullable = False)

    def _init_(self, titulo, autor, ano, genero, editora):
        self.titulo = titulo
        self.autor = autor
        self.ano = ano
        self.genero = genero
        self.editora = editora

class Usuario(db.Model):
    _tablename_='usuarios'

    id = db.Column(db.Integer, primary_key = True,
                   autoincrement = True, nullable=False, unique=True)
    nome = db.Column(db.String,  nullable = False)
    email = db.Column(db.String,  nullable = False)
    telefone = db.Column(db.String,  nullable = False)
    senha = db.Column(db.String,  nullable = False)

    def _init_(self, nome, email, telefone, senha):
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.senha = senha

class Reserva_livro(db.Model):
    _tablename_='reservas'

    id = db.Column(db.Integer, primary_key = True,
                   autoincrement = True, nullable=False, unique=True)
    id_livro = db.Column(db.Integer, db.ForeignKey('livros.id'),
                         nullable = False)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'),
                           nullable = False)

    livro = db.relationship('Livro',
                            backref=db.backref('reservas', lazy = False))
    usuario = db.relationship('Usuario',
                              backref=db.backref('reservas', lazy = False))

    _table_args_ = (db.UniqueConstraint('id_livro', 'id_usuario',
                                        name='unique_reserva'))

    def _init_(self, id_livro, id_usuario):
        self.id_livro = id_livro
        self.id_usuario = id_usuario

class ListaEspera(db.Model):
    __tablename__='lista_espera'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True,
                   nullable = False, unique = True)
    id_livro = db.Column(db.Integer, db.ForeignKey('livros.id'),
                         nullable = False)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'),
                           nullable = False)


    livro = db.relationship(db.Integer, db.ForeignKey('livros.id'),
                            backref=db.backref('lista_espera', lazy = True))
    usuario = db.relationship(db.Integer, db.ForeignKey('usuarios.id'),
                              backref=db.backref('lista_espera', lazy = True))


    def __init__(self, id_livro, id_usuario):
        self.id_livro = id_livro
        self.id_usuario = id_usuario