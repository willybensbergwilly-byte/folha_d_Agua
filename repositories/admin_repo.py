from database.conexao import conectar

def tabela_admin():
    conexao = conectar()
    cursor = conexao.cursor()

    criar_tabela_admin = """
    CREATE TABLE IF NOT EXISTS tabela_admin (
        id INT AUTO_INCREMENT PRIMARY KEY,
        usuario VARCHAR(50) NOT NULL UNIQUE,
        senha_hash VARCHAR(255) NOT NULL
    )
    """

    cursor.execute(criar_tabela_admin)
    conexao.commit()

def buscar_admin(usuario):
    conexao = conectar()
    cursor = conexao.cursor()
    try:
        cursor.execute(
            "SELECT id, usuario, senha_hash FROM tabela_admin WHERE usuario = %s LIMIT 1",
            (usuario,)
        )
        return cursor.fetchone()
    finally:
        cursor.close()
        conexao.close()

def cadastrar_admin(usuario, senha_hash):
    conexao = conectar()
    cursor = conexao.cursor()
    try:
        cursor.execute(
            "INSERT INTO tabela_admin (usuario, senha_hash) VALUES (%s, %s)",
            (usuario, senha_hash)
        )
        conexao.commit()
    finally:
        cursor.close()
        conexao.close()
