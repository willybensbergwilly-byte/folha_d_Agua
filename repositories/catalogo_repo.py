
from database.conexao import conectar


def tabela_catalogo():
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        # Cria a tabela de categorias, caso não exista.
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS categoria (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(50) NOT NULL UNIQUE
            )
        """)

        # Cadastra as três categorias sem duplicá-las.
        cursor.execute("""
            INSERT IGNORE INTO categoria (nome)
            VALUES ('Buquê'), ('Arranjo'), ('Flor individual')
        """)

        # Cria o catálogo com relacionamento para bancos novos.
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS catalogo (
                id INT AUTO_INCREMENT PRIMARY KEY,
                tipo_produto VARCHAR(17) NOT NULL,
                nome_flor VARCHAR(150) NOT NULL,
                preco DECIMAL(10,2) NOT NULL,
                estoque INT NOT NULL,
                imagem VARCHAR(255) NULL,
                categoria_id INT NULL,

                CONSTRAINT fk_catalogo_categoria
                FOREIGN KEY (categoria_id)
                REFERENCES categoria(id)
            )
        """)

        # Compatibilidade com tabelas antigas sem imagem.
        cursor.execute("SHOW COLUMNS FROM catalogo LIKE 'imagem'")

        if cursor.fetchone() is None:
            cursor.execute("""
                ALTER TABLE catalogo
                ADD COLUMN imagem VARCHAR(255) NULL
            """)

        conexao.commit()

    finally:
        cursor.close()
        conexao.close()


def cadastrar_produto(tipo_produto, nome_flor, preco, estoque, imagem=None):
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        # Busca o ID da categoria pelo nome selecionado no HTML.
        cursor.execute("""
            SELECT id FROM categoria
            WHERE nome = %s
        """, (tipo_produto,))

        categoria = cursor.fetchone()

        if categoria is None:
            raise ValueError("Categoria de produto inválida.")

        categoria_id = categoria[0]

        # Cadastra o produto com sua chave estrangeira.
        cursor.execute("""
            INSERT INTO catalogo
            (tipo_produto, nome_flor, preco, estoque, imagem, categoria_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            tipo_produto,
            nome_flor,
            preco,
            estoque,
            imagem,
            categoria_id
        ))

        conexao.commit()
        return cursor.lastrowid

    finally:
        cursor.close()
        conexao.close()


def listar_produtos():
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute("""
            SELECT id, tipo_produto, nome_flor, preco, estoque, imagem
            FROM catalogo
            ORDER BY nome_flor
        """)

        return cursor.fetchall()

    finally:
        cursor.close()
        conexao.close()


def buscar_produto(id):
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute("""
            SELECT id, tipo_produto, nome_flor, preco, estoque, imagem
            FROM catalogo
            WHERE id = %s
        """, (id,))

        return cursor.fetchone()

    finally:
        cursor.close()
        conexao.close()


def atualizar_estoque(id, estoque):
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute("""
            UPDATE catalogo
            SET estoque = %s
            WHERE id = %s
        """, (estoque, id))

        conexao.commit()

        if cursor.rowcount > 0:
            return True

        # Confere se o produto existe, mesmo sem alteração.
        cursor.execute("""
            SELECT id FROM catalogo WHERE id = %s
        """, (id,))

        return cursor.fetchone() is not None

    finally:
        cursor.close()
        conexao.close()


def editar_produto(id, tipo_produto, nome_flor, preco, estoque, imagem=None):
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        # Busca o ID correspondente à categoria selecionada.
        cursor.execute("""
            SELECT id FROM categoria
            WHERE nome = %s
        """, (tipo_produto,))

        categoria = cursor.fetchone()

        if categoria is None:
            raise ValueError("Categoria de produto inválida.")

        categoria_id = categoria[0]

        # Atualiza os dados e a categoria do produto.
        cursor.execute("""
            UPDATE catalogo
            SET tipo_produto = %s,
                nome_flor = %s,
                preco = %s,
                estoque = %s,
                imagem = COALESCE(%s, imagem),
                categoria_id = %s
            WHERE id = %s
        """, (
            tipo_produto,
            nome_flor,
            preco,
            estoque,
            imagem,
            categoria_id,
            id
        ))

        conexao.commit()
        return cursor.rowcount > 0

    finally:
        cursor.close()
        conexao.close()


def deletar_produto(id):
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute("""
            DELETE FROM catalogo WHERE id = %s
        """, (id,))

        conexao.commit()
        return cursor.rowcount > 0

    finally:
        cursor.close()
        conexao.close()
