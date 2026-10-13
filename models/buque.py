from models.catalogo.catalogo import Catalogo


class Buque(Catalogo):
    def __init__(self, nome_flor, preco):
        super().__init__("Buquê", nome_flor, preco)