
"""
Folha D'Água — Inicialização do banco de dados.

Executar na raiz do projeto:
    python seed.py

Funcionalidades:
- Criar o banco MySQL, caso não exista.
- Criar as tabelas usando os repositórios existentes.
- Popular a tabela de categorias.
- Verificar a estrutura do catálogo.
- Corrigir o tipo da coluna estoque, quando seguro.
- Cadastrar o primeiro administrador.
"""

import os
import re
from getpass import getpass

import mysql.connector
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash

from database.conexao import conectar

from repositories.admin_repo import (
    tabela_admin,
    buscar_admin,
    cadastrar_admin
)

from repositories.catalogo_repo import tabela_catalogo
from repositories.cliente_repo import tabela_cliente
from repositories.encomenda_repo import tabela_encomenda


load_dotenv()


# ==========================================
# CONFIGURAÇÕES
# ==========================================

NOME_BANCO = os.getenv("DB_NAME", "folha_dagua")

DADOS = {
    "categoria": [
        "Buquê",
        "Arranjo",
        "Flor individual"
    ]
}


# ==========================================
# 1. CRIAR BANCO DE DADOS
# ==========================================

def criar_banco():

    if not re.fullmatch(r"[A-Za-z0-9_]+", NOME_BANCO):
        raise ValueError("Nome do banco de dados inválido.")

    print("\n=== Verificando banco de dados ===")

    conexao = mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "")
    )

    cursor = conexao.cursor()

    try:
        cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS `{NOME_BANCO}` "
            "CHARACTER SET utf8mb4 "
            "COLLATE utf8mb4_unicode_ci"
        )

        conexao.commit()

        print(f"Banco '{NOME_BANCO}' verificado/criado.")

    finally:
        cursor.close()
        conexao.close()


# ==========================================
# 2. CRIAR TABELAS
# ==========================================

def criar_tabelas():

    print("\n=== Verificando tabelas ===")

    tabela_catalogo()
    print("Tabelas categoria e catalogo verificadas.")

    tabela_admin()
    print("Tabela tabela_admin verificada.")

    tabela_cliente()
    print("Tabela cliente verificada.")

    tabela_encomenda()
    print("Tabela encomenda verificada.")

    print("\nTabelas verificadas/criadas com sucesso!")


# ==========================================
# 3. POPULAR TABELAS
# ==========================================

def popular_tabela(tabela, nomes):

    # Permitir somente a tabela conhecida pelo projeto.
    if tabela != "categoria":
        raise ValueError("Tabela não autorizada para popular.")

    conexao = conectar()
    cursor = conexao.cursor()

    try:

        for nome in nomes:

            cursor.execute(
                "SELECT id FROM categoria WHERE nome = %s",
                (nome,)
            )

            existente = cursor.fetchone()

            if existente is None:

                cursor.execute(
                    "INSERT INTO categoria (nome) VALUES (%s)",
                    (nome,)
                )

                print(f"  + {tabela}: {nome}")

        conexao.commit()

    finally:
        cursor.close()
        conexao.close()


# ==========================================
# 4. VERIFICAR ESTRUTURA DO CATÁLOGO
# ==========================================

def verificar_catalogo():

    print("\n=== Verificando estrutura do catálogo ===")

    conexao = conectar()
    cursor = conexao.cursor()

    try:

        cursor.execute("SHOW COLUMNS FROM catalogo")

        colunas = {
            coluna[0]: coluna[1]
            for coluna in cursor.fetchall()
        }

        # Verificar coluna imagem.
        if "imagem" not in colunas:

            cursor.execute("""
                ALTER TABLE catalogo
                ADD COLUMN imagem VARCHAR(255) NULL
            """)

            print("Coluna imagem adicionada.")

        else:
            print("Coluna imagem já existe.")

        # Verificar coluna categoria_id.
        if "categoria_id" not in colunas:

            print(
                "AVISO: coluna categoria_id não encontrada. "
                "É necessária uma migração para adicionar "
                "a chave estrangeira."
            )

        else:
            print("Coluna categoria_id encontrada.")

        # Verificar tipo do estoque.
        tipo_estoque = colunas.get("estoque", "")

        if tipo_estoque.lower().startswith("int"):

            print("Coluna estoque já utiliza INT.")

        elif tipo_estoque:

            print(
                f"Estoque utiliza atualmente: {tipo_estoque}"
            )

            cursor.execute("""
                SELECT id, estoque
                FROM catalogo
            """)

            registros = cursor.fetchall()

            valores_validos = True

            for id_produto, estoque in registros:

                valor = str(estoque)

                if (
                    not valor.isdecimal()
                    or int(valor) > 2147483647
                ):
                    valores_validos = False

                    print(
                        "Estoque inválido encontrado "
                        f"no produto ID {id_produto}: {estoque}"
                    )

            if valores_validos:

                cursor.execute("""
                    ALTER TABLE catalogo
                    MODIFY COLUMN estoque INT NOT NULL
                """)

                print(
                    "Coluna estoque convertida para INT."
                )

            else:

                print(
                    "Conversão cancelada. "
                    "Corrija os valores inválidos antes."
                )

        else:
            print("AVISO: coluna estoque não encontrada.")

        conexao.commit()

    finally:
        cursor.close()
        conexao.close()


# ==========================================
# 5. CRIAR ADMINISTRADOR INICIAL
# ==========================================

def criar_admin_inicial():

    print("\n=== Administrador inicial ===")

    conexao = conectar()
    cursor = conexao.cursor()

    try:

        cursor.execute("""
            SELECT usuario
            FROM tabela_admin
            LIMIT 1
        """)

        existente = cursor.fetchone()

    finally:
        cursor.close()
        conexao.close()

    if existente:

        print(
            f"Já existe um administrador: {existente[0]}"
        )

        print("Nenhum administrador foi alterado.")

        return

    print("\nNenhum administrador encontrado.")
    print("Vamos cadastrar o primeiro administrador.")

    usuario = input(
        "Usuário (3 a 50 caracteres): "
    ).strip()

    if not 3 <= len(usuario) <= 50:

        print(
            "Usuário inválido. "
            "Informe entre 3 e 50 caracteres."
        )

        return

    if buscar_admin(usuario):

        print(
            "Esse usuário já existe. "
            "Nenhuma alteração foi feita."
        )

        return

    senha = getpass(
        "Senha (mínimo de 12 caracteres): "
    )

    confirmar = getpass(
        "Confirme a senha: "
    )

    if len(senha) < 12:

        print(
            "A senha precisa ter pelo menos "
            "12 caracteres."
        )

        return

    if senha != confirmar:

        print("As senhas não coincidem.")

        return

    senha_hash = generate_password_hash(senha)

    cadastrar_admin(usuario, senha_hash)

    print(
        f"\nAdministrador '{usuario}' "
        "cadastrado com sucesso!"
    )


# ==========================================
# 6. EXECUTAR INICIALIZAÇÃO
# ==========================================

def main():

    print("=" * 50)
    print("       FOLHA D'ÁGUA - DATABASE SEED")
    print("=" * 50)

    try:

        criar_banco()

        criar_tabelas()

        for tabela, nomes in DADOS.items():
            popular_tabela(tabela, nomes)

        verificar_catalogo()

        criar_admin_inicial()

        print("\n" + "=" * 50)
        print("Inicialização concluída com sucesso!")
        print("=" * 50)

    except mysql.connector.Error as erro:

        print("\nERRO NO MYSQL:")
        print(erro)

    except Exception as erro:

        print("\nERRO NA INICIALIZAÇÃO:")
        print(erro)


if __name__ == "__main__":
    main()
