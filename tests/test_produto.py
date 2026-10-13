import pytest
from models.catalogo.catalogo import Catalogo
from models.buque import Buque
from models.arranjo import Arranjo


def test_heranca_e_tipos():
    assert isinstance(Buque("Rosas", 50), Catalogo)
    assert isinstance(Arranjo("Lírios", 80), Catalogo)
    assert Buque("Rosas", 50).tipo_produto == "Buquê"
    assert Arranjo("Lírios", 80).tipo_produto == "Arranjo"


def test_encapsulamento_e_preco():
    produto = Catalogo("Flor individual", "Rosa", 12.5)
    assert "R$ 12.50" in str(produto)
    with pytest.raises(ValueError):
        produto.preco = -5
