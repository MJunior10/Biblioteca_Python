from flask import Flask, request, redirect, url_for, jsonify, flash
from models import db, Livro, Usuario, Reserva_livro,ListaEspera
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@localhost:5433/biblioteca'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bcrypt = Bcrypt(app)

try:
    db.init_app(app)
except Exception as e:
    print(f'Não foi possível inicializar o banco de dados: {e}')


@app.route("/")
def index():
    return "Home"


@app.route('/cadastro_livros', methods=['POST'])
def cadastro_livros():
    try:
        titulo = request.form['titulo']
        autor = request.form['autor']
        ano = request.form['ano']
        genero = request.form['genero']
        editora = request.form['editora']
        livro = Livro(titulo, autor, ano, genero, editora)

        db.session.add(livro)
        db.session.commit()
        print('Livro cadastrado com sucesso')
        return redirect(url_for('index'))

    except KeyError as e:
        return jsonify({"error": f"Campo Ausente{e}"}), 400
    except Exception as e:
        return jsonify({'error': f"Erro ao cadastrar livro: {e}"}), 500

@app.route('/editar_livros', methods=['POST'])
def editar_livros():
    try:

        id = request.form['id']
        livro = Livro.query.filter_by(id=id).first()
        if livro :

            titulo = request.form['titulo']
            autor = request.form['autor']
            ano = request.form['ano']
            genero = request.form['genero']
            editora = request.form['editora']

            livro.titulo = titulo
            livro.autor = autor
            livro.ano = ano
            livro.genero = genero
            livro.editora = editora

            db.session.commit()
            print('Livro editado com sucesso')
            return redirect(url_for('index'))

        else:
            return jsonify({"error": "Livro não Encontrado"}), 404
    except KeyError as e:
        return jsonify({"error": f"Campo Ausente{e}"}), 400
    except Exception as e:
        return jsonify({"error": f"Erro ao editar livro:{e}"}), 500

@app.route('/localizar_livros', methods=['POST'])
def localizar_livros():
    try:
        id = request.form['id']
        livro = Livro.query.filter_by(id=id).first()

        if livro is None:
            return jsonify({'menssage:'}, 'Livro não encontrado'), 404

        resultado = {
            "titulo": livro.titulo,
            "autor": livro.autor,
            "ano": livro.ano,
            "genero": livro.genero,
            "editora": livro.editora
        }

        return jsonify(resultado), 200

    except KeyError as e:
        return jsonify({"error": f"Campo Ausente{e}"}), 400
    except Exception as e:
        return jsonify({"error": f"Erro ao deletar livro:{e}"}), 500

@app.route('/deletar_livros', methods = ['POST'])
def deletar_livros():
    try:
        id = request.form['id']
        livro = Livro.query.filter_by(id=id).first()

        if livro :
            db.session.delete(livro)
            db.session.commit()
            print('Livro deletado com sucesso')
            return redirect(url_for('index'))
        else:
            return jsonify({"error": 'Livro não encontrado'})
    except KeyError as e:
        return jsonify({"error": f"Campo Ausente{e}"}), 400
    except Exception as e:
        return jsonify({"error": f"Erro ao deletar livro:{e}"}), 500

@app.route('/cadastrar_usuarios', methods=['POST'])
def cadastrar_usuarios():
    try:
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        senha = request.form['senha']
        hashed_senha = bcrypt.hashpw(senha, bcrypt.gensalt()).decode('utf-8')
        usuario = Usuario(nome, email, telefone, hashed_senha)

        db.session.add(usuario)
        db.session.commit()

        print('Usuario cadastrado com sucesso')
        return redirect(url_for('index'))

    except KeyError as e:
        return jsonify({"error": f"Campo Ausente{e}"}), 400
    except Exception as e:
        return jsonify({"error": "Erro ao cadastrar usuario:{e}"}), 500

@app.route('/editar_usuarios', methods=['POST'])
def editar_usuarios():
    try:
        id = request.form.get('id')
        if not id:
            return jsonify({"message": "ID do usuario não fornecido"}), 400
        
        user = Usuario.query.get(id)
        if user:

            nome = request.form.get('nome')
            email = request.form.get('email')
            telefone = request.form.get('telefone')
            senha = request.form.get('senha')

            if nome:
                user.nome = nome
            if email:
                user.email = email
            if telefone:
                user.telefone = telefone
            if senha:
                hashed_senha = bcrypt.generate_password_hash(senha).decode('utf-8')
                user.senha = hashed_senha

            db.session.commit()
            return jsonify({"message": "Usuário atualizado com sucesso"}), 200
        else:
            return jsonify({"error": "Usuário não encontrado"}), 404

    except Exception as e:
        return jsonify({"error": f"Erro ao editar usuário: {str(e)}"}), 500

@app.route('/login', methods=['POST'])
def login():
    try:
        usuario = request.form['usuario']
        senha = request.form['senha']
        user = Usuario.query.filter_by(usuario=usuario).first()

        if user and bcrypt.check_password_hash(user.hashed_password, senha):
            flash('Logado com sucesso')
            return redirect(url_for('index'))
        else:
            flash('Senha incorretos')
            return redirect(url_for('login'))
    except KeyError as e:
        return jsonify({"error": f"Campo Ausente{e}"}), 400
    except Exception as e:
        return jsonify({"error": f"Erro ao logar usuario:{e}"}), 500

@app.route('/logout')
def logout():
    return redirect(url_for('home'))

@app.route('/reserva_livros', methods=['POST'])
def reserva_livros():
    try:
        id_livro = request.form['id_livro']
        id_usuario = request.form['id_usuario']

        reserva_livro = Reserva_livro.query.filter_by(id_livro=id_livro).first()
        if reserva_livro is None:
            reserva = Reserva_livro(id_livro, id_usuario)
            db.session.add(reserva)
            db.session.commit()
            print('Reserva cadastrada com sucesso')
            return redirect(url_for('index'))
        else:
            return jsonify({"Livro já está reservado"}), 200
    except KeyError as e:
        return jsonify({"error": f"Campo Ausente{e}"}), 400
    except Exception as e:
        return jsonify({"error": f"Erro ao reservar livro:{e}"}), 500

@app.route('/entrar_fila_espera', methods=['POST'])
def entrar_fila_espera():
    try:
        id_livro = request.form['id_livro']
        id_usuario = request.form['id_usuario']

        resultado = lista_espera(id_usuario, id_livro)
        return jsonify(resultado)

    except KeyError as e:
        return jsonify({"error": f"Campo Ausente{e}"}), 400
    except Exception as e:
        return jsonify({"error": f"Erro ao entrar na fila de espera: {e}"}), 500


def lista_espera(id_usuario, id_livro):

    usuario = Usuario.query.filter_by(id=id_usuario).first()
    livro = Livro.query.filter_by(id=id_livro).first()

    if  usuario and livro:
        nova_reserva = ListaEspera(id_livro, id_usuario)
        db.session.add(nova_reserva)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        return jsonify({"error": "Usuário ou livro não encontrado"}), 404


def reservasporlivro(id_livro):
    livro = Livro.query.get(id_livro)
    if livro:
        reservas = livro.reservas
        if reservas:

            return jsonify([{"id_usuario": reserva.id_usuario, "data_reserva":
                reserva.data_reserva} for reserva in reservas])
        else:
            return jsonify({"message": "Este livro não possui reservas"}), 200
    else:
        return jsonify({"error": "Livro não encontrado"}), 404

@app.route('/catalogo_genero', methods=['POST'])
def catalogo():
    try:  
        genero = request.form.get('genero')
        if genero:
            livros = Livro.query.filter_by(genero=genero).all()
            if livros:
                resultado = [
                    {
                        "id": livro.id,
                        "titulo": livro.titulo,
                        "autor": livro.autor,
                        "ano": livro.ano,
                        "genero": livro.genero,
                        "editora": livro.editora
                    }
                    for livro in livros
                ]

                return jsonify(resultado), 200
            else: 
                return jsonify({"message": "Não foram;. encontrados livros nesse genero"}), 404
        else:
            return jsonify({"error": "Genero não fornecido"}), 400
    except Exception as e:
        return jsonify({"error": f"Erro ao buscar livros: {str(e)}"}), 500
        
@app.route('/catalogo_geral', methods=['POST'])
def lista_livros():
    try:
        if livros:
            livros = Livro,query.all()
            return (livros), 200
        else: 
            return jsonify({"message": "Não existe nenhum livro cadastrado"})
    except Exception as e:
        return jsonify({"error:", f"Erro ao listar livros: {str(e)}"})

if __name__ == '__main__':
    with app.app_context():
        try:
         db.create_all()
        except Exception as e:
            print(f'Não foi possivel criar o banco de dados {e}')
    app.run(debug=True)