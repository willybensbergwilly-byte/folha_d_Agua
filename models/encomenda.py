class Encomenda:
    def __init__(self, data_pedido_realizado, data_retirado, nome_cliente,
                 tipo_pedido, quantidade, status):
        self.data_pedido_realizado = data_pedido_realizado
        self.data_retirado = data_retirado
        self.nome_cliente = nome_cliente
        self.tipo_pedido = tipo_pedido
        self.quantidade = quantidade
        self.status = status

    def __str__(self):
        return (
            f"Data do Pedido: {self.data_pedido_realizado} | "
            f"Data de Retirada: {self.data_retirado} | "
            f"Cliente: {self.nome_cliente} | "
            f"Tipo de Pedido: {self.tipo_pedido} | "
            f"Quantidade: {self.quantidade} | "
            f"Status: {self.status}"
        )
