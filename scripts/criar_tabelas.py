"""Execute na raiz do projeto: python -m scripts.criar_tabelas"""
from repositories.admin_repo import tabela_admin
from repositories.catalogo_repo import tabela_catalogo
from repositories.cliente_repo import tabela_cliente
from repositories.encomenda_repo import tabela_encomenda


def main():
    tabela_catalogo()
    tabela_admin()
    tabela_cliente()
    tabela_encomenda()
    print("Tabelas verificadas/criadas no MySQL.")


if __name__ == "__main__":
    main()
