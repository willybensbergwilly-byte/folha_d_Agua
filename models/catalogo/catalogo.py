class Catalogo:
    """Classe mãe para buquês, arranjos e flores individuais."""

    def __init__(self, tipo_produto, nome_flor, preco):
        self.tipo_produto = tipo_produto
        self.nome_flor = nome_flor
        self.preco = preco

    @property
    def preco(self):
        return self._preco

    @preco.setter
    def preco(self, valor):
        valor = float(valor)
        if valor <= 0:
            raise ValueError("O preço deve ser maior que zero.")
        self._preco = valor

    @property
    def nome_flor(self):
        return self._nome_flor

    @nome_flor.setter
    def nome_flor(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("O nome do produto é obrigatório.")
        self._nome_flor = valor.strip()

    def __str__(self):
        return (
            f"Tipo de Produto: {self.tipo_produto} | "
            f"Nome: {self.nome_flor} | "
            f"Preço: R$ {self.preco:.2f}"
        )
