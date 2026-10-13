from database.conexao import conectar

def tabela_cliente():
    conexao = conectar()
    cursor = conexao.cursor()
    
    criar_tabela_cliente = """
        CREATE TABLE IF NOT EXISTS cliente (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(140) NOT NULL,
            email VARCHAR(150) NOT NULL UNIQUE,
            senha_hash VARCHAR(255) NOT NULL,
            telefone VARCHAR(16) NOT NULL   
        )
    """
    
    cursor.execute(criar_tabela_cliente)
    conexao.commit()

    cursor.close()
    conexao.close()

    print("tabela criada com sucesso!!")