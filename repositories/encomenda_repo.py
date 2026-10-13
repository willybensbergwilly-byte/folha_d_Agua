from database.conexao import conectar

def tabela_encomenda():
    conexao = conectar()
    cursor = conexao.cursor()

    criar_tabela_encomenda = """
        CREATE TABLE IF NOT EXISTS encomenda (
            id INT AUTO_INCREMENT PRIMARY KEY,
            data_pedido_realizado DATE NOT NULL,
            data_retirado DATE NOT NULL,
            nome_cliente VARCHAR(255) NOT NULL,
            tipo_produto VARCHAR(255) NOT NULL,
            quantidade INT NOT NULL,
            status VARCHAR(50) NOT NULL
        )
    """

    cursor.execute(criar_tabela_encomenda)
    conexao.commit()

    cursor.close()
    conexao.close()