from flask import Flask,redirect,url_for,render_template,request,flash,session
from werkzeug.security import generate_password_hash,check_password_hash
app = Flask("__main__")
app.secret_key = "123"
@app.route("/")
def main():
    return redirect(url_for("home"))

@app.route("/home")
def home():
    return render_template("home.html",usuario = "Carlos")

@app.route("/cadastro",methods=["GET","POST"])
def cadastro():
    if request.method == "POST":
        usuario = request.form["nome"]
        senha = request.form["senha"]
        senha_hash = generate_password_hash(senha)
        import sqlite3 
        conn = sqlite3.connect("usuarios.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios(usuario,senha) VALUES (?,?)", (usuario,senha_hash))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for("login"))
    return render_template("cadastro.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        usuario = request.form["nome"]
        senha = request.form["senha"]
        import sqlite3 
        conn = sqlite3.connect("usuarios.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios where usuario = ?",(usuario,))
        dados = cursor.fetchall()[0]
        cursor.close()
        conn.close()
        if( check_password_hash(dados[2],senha) and usuario == dados[1]):
            session["usuario"] = dados[1]
            return redirect(url_for("home"))
        else:
            flash("Usuario ou senha incorretos","erro")
            return redirect(url_for("login"))
    return render_template("login.html")
@app.route("/noticias")
def noticias():
    return render_template("noticias.html")

@app.route("/revistas")
def revistas():
    import sqlite3 
    conn = sqlite3.connect("revistas.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM revistas")
    revistas = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("revistas.html",revistas=revistas)
@app.route("/adicionar_revista", methods=["GET","POST"])
def adicionar_revista():
    if request.method == "POST":
        titulo = request.form["titulo"]
        descricao = request.form["descricao"]
        import sqlite3 
        conn = sqlite3.connect("revistas.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO revistas(titulo,descricao) VALUES (?,?)",(titulo,descricao))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for("revistas"))
    return render_template("adicionar_revista.html",revistas=revistas)
@app.route("/musicos")
def musicos():
    import sqlite3 
    conn = sqlite3.connect("musicos.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM musicos")
    musicos = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("musicos.html",musicos=musicos)
@app.route("/adicionar_musico",methods=["POST","GET"])
def adicionar_musico():
    if request.method=="POST":
        nome = request.form["nome"]
        idade = request.form["idade"]
        funcao = request.form["funcao"]
        imagem = request.form["imagem"]
        import sqlite3 
        conn = sqlite3.connect("musicos.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO musicos(nome,idade,funcao,imagem) VALUES (?,?,?,?)",(nome,idade,funcao,imagem))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for("musicos"))
    return render_template("adicionar_musico.html")
if __name__ == "__main__":
    app.run(debug=True)