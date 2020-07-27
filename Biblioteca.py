import sqlite3
conexao = sqlite3.connect('biblioteca.db')
cursor = conexao.cursor()
cursor.executescript(open("createBiblioteca.sql").read())
conexao.commit()
cursor.close()
conexao.close()

