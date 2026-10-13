import pytest
from models.cliente import Cliente


def test_cliente_e_email_encapsulado():
    cliente = Cliente(1, "hash", "Maria", "maria@email.com", "41999999999")
    assert cliente.email == "maria@email.com"
    assert "Maria" in str(cliente)
    with pytest.raises(ValueError):
        cliente.email = "invalido"
