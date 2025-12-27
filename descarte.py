import sqlite3

# Conecta ao banco de dados
conexao = sqlite3.connect("revistas.db")
cursor = conexao.cursor()

# Atualiza a imagem da revista com id = 1
cursor.execute("""
UPDATE revistas
SET link = ?
WHERE id = ?
""", ("https://almanaquesambadeterreiro.netlify.app/", 1))

# Salva e fecha
conexao.commit()
conexao.close()

print("Imagem adicionada com sucesso na revista de id = 1")
