
from getpass import getpass
from werkzeug.security import generate_password_hash, check_password_hash

from database.conexao import conectar
from repositories.admin_repo import buscar_admin


def alterar_senha():
    usuario = input("Usuário administrador: ").strip()
    senha_atual = getpass("Senha atual: ")

    admin = buscar_admin(usuario)

    if not admin or not check_password_hash(admin[2], senha_atual):
        print("Usuário ou senha atual incorretos.")
        return

    nova_senha = getpass("Nova senha: ")
    confirmar = getpass("Confirme a nova senha: ")

    if len(nova_senha) < 12:
        print("A nova senha precisa ter pelo menos 12 caracteres.")
        return

    if nova_senha != confirmar:
        print("As senhas não coincidem.")
        return

    senha_hash = generate_password_hash(nova_senha)

    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute("""
            UPDATE tabela_admin
            SET senha_hash = %s
            WHERE id = %s
        """, (senha_hash, admin[0]))

        conexao.commit()
        print("Senha alterada com sucesso!")

    finally:
        cursor.close()
        conexao.close()


if __name__ == "__main__":
    alterar_senha()
