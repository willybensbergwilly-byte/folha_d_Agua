"""Executar na raiz do projeto: python -m scripts.criar_admin"""
from getpass import getpass
from werkzeug.security import generate_password_hash
from repositories.admin_repo import buscar_admin, cadastrar_admin, tabela_admin


def main():
    tabela_admin()
    print("=== Criar administrador do Folha D'Água ===")
    usuario = input("Usuário (3 a 50 caracteres): ").strip()
    if not 3 <= len(usuario) <= 50:
        print("Usuário inválido.")
        return
    if buscar_admin(usuario):
        print("Esse usuário já existe. Nenhuma alteração foi feita.")
        return
    senha = getpass("Senha (pelo menos 12 caracteres): ")
    confirmar = getpass("Confirme a senha: ")
    if len(senha) < 12 or senha != confirmar:
        print("As senhas devem ser iguais e ter no mínimo 12 caracteres.")
        return
    cadastrar_admin(usuario, generate_password_hash(senha))
    print("Administrador cadastrado com sucesso! Você já pode fazer login.")


if __name__ == "__main__":
    main()
