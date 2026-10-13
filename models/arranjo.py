from models.catalogo.catalogo import Catalogo


class Arranjo(Catalogo):
    def __init__(self, nome_flor, preco):
        super().__init__("Arranjo", nome_flor, preco)