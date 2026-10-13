from models.admin.admin import Admin
from models.estoque import Estoque
from models.buque import Buque


def test_admin_e_estoque():
    admin = Admin("gerente", "hash")
    assert admin.usuario_admin == "gerente"
    estoque = Estoque(Buque("Margaridas", 30), 9)
    assert "Quantidade em estoque: 9" in str(estoque)
