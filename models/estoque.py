class Estoque:
    def __init__(self, produto, quantidade):
        self.produto = produto
        self.quantidade = quantidade

    def __str__(self):
        return (
            f"Produto: {self.produto.nome_flor} | "
            f"Quantidade em estoque: {self.quantidade}"
        )