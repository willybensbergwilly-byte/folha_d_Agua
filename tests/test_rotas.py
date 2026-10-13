
from io import BytesIO

import pytest
import app as site


@pytest.fixture
def cliente_flask(monkeypatch, tmp_path):
    site.app.config.update(TESTING=True)

    # Nenhuma conexão real com o MySQL.
    monkeypatch.setattr(
        site.app,
        "static_folder",
        str(tmp_path)
    )

    monkeypatch.setattr(
        site,
        "listar_produtos",
        lambda: []
    )

    return site.app.test_client()


@pytest.fixture
def cliente_admin(cliente_flask):
    # Simula um administrador autenticado.
    with cliente_flask.session_transaction() as sessao:
        sessao["admin_id"] = 1

    return cliente_flask


def test_catalogo_vazio_carrega(cliente_flask):
    resposta = cliente_flask.get("/")

    assert resposta.status_code == 200
    assert (
        "Nenhum produto encontrado nesta categoria."
        in resposta.get_data(as_text=True)
    )


def test_cadastro_com_imagem(cliente_admin, monkeypatch, tmp_path):
    recebido = []

    monkeypatch.setattr(
        site,
        "cadastrar_produto",
        lambda *args: recebido.append(args)
    )

    dados = {
        "tipo_produto": "Buquê",
        "nome_flor": "Rosas",
        "preco": "39.90",
        "estoque": "10",
        "imagem": (
            BytesIO(b"\x89PNG\r\n\x1a\n" + b"0" * 20),
            "foto.png"
        ),
    }

    resposta = cliente_admin.post(
        "/admin/produtos/cadastrar",
        data=dados,
        content_type="multipart/form-data"
    )

    assert resposta.status_code == 302
    assert len(recebido) == 1
    assert recebido[0][-1].endswith(".png")

    assert (
        tmp_path / "img" / "produtos" / recebido[0][-1]
    ).exists()


def test_edicao_troca_imagem(cliente_admin, monkeypatch, tmp_path):
    recebido = []
    antigo = "antigo.jpg"

    pasta = tmp_path / "img" / "produtos"
    pasta.mkdir(parents=True)

    (pasta / antigo).write_bytes(b"foto antiga")

    monkeypatch.setattr(
        site,
        "buscar_produto",
        lambda id: (id, "Arranjo", "Lirios", 50, 4, antigo)
    )

    monkeypatch.setattr(
        site,
        "editar_produto",
        lambda *args: recebido.append(args)
    )

    dados = {
        "tipo_produto": "Arranjo",
        "nome_flor": "Lirios",
        "preco": "75.00",
        "estoque": "5",
        "imagem": (
            BytesIO(b"\x89PNG\r\n\x1a\n" + b"0" * 20),
            "nova.png"
        ),
    }

    assert (
        cliente_admin.get("/admin/estoque/editar/2").status_code
        == 200
    )

    resposta = cliente_admin.post(
        "/admin/estoque/editar/2",
        data=dados,
        content_type="multipart/form-data"
    )

    assert resposta.status_code == 302
    assert len(recebido) == 1
    assert recebido[0][-1].endswith(".png")
    assert (pasta / recebido[0][-1]).exists()
    assert not (pasta / antigo).exists()


def test_edicao_sem_imagem_mantem_antiga(
    cliente_admin,
    monkeypatch
):
    recebido = []

    monkeypatch.setattr(
        site,
        "buscar_produto",
        lambda id: (
            id, "Buquê", "Rosas", 90, 5, "antiga.jpg"
        )
    )

    monkeypatch.setattr(
        site,
        "editar_produto",
        lambda *args: recebido.append(args)
    )

    resposta = cliente_admin.post(
        "/admin/estoque/editar/4",
        data={
            "tipo_produto": "Buquê",
            "nome_flor": "Rosas",
            "preco": "90.00",
            "estoque": "6"
        }
    )

    assert resposta.status_code == 302
    assert len(recebido) == 1
    assert recebido[0][-1] is None


def test_formulario_de_edicao_tem_upload_dentro_do_form(
    cliente_admin,
    monkeypatch
):
    monkeypatch.setattr(
        site,
        "buscar_produto",
        lambda id: (id, "Buquê", "Rosas", 90, 5, None)
    )

    pagina = cliente_admin.get(
        "/admin/estoque/editar/4"
    ).get_data(as_text=True)

    assert 'enctype="multipart/form-data"' in pagina

    assert (
        pagina.index("<form ")
        < pagina.index('name="imagem"')
        < pagina.index("</form>")
    )


def test_estoque_links_e_produtos(cliente_admin, monkeypatch):
    monkeypatch.setattr(
        site,
        "listar_produtos",
        lambda: [
            (
                7,
                "Flor individual",
                "Tulipa",
                15.5,
                12,
                "tulipa.png"
            )
        ]
    )

    resposta = cliente_admin.get("/admin/estoque")
    pagina = resposta.get_data(as_text=True)

    assert resposta.status_code == 200
    assert 'href="/admin/estoque/editar/7"' in pagina
    assert 'action="/admin/estoque/deletar/7"' in pagina
    assert "Tulipa" in pagina


def test_catalogo_link_imagem_e_whatsapp(
    cliente_flask,
    monkeypatch
):
    monkeypatch.setattr(
        site,
        "listar_produtos",
        lambda: [
            (
                10,
                "Arranjo",
                "Violetas",
                78.5,
                3,
                "violetas.jpg"
            )
        ]
    )

    resposta = cliente_flask.get("/")
    pagina = resposta.get_data(as_text=True)

    assert resposta.status_code == 200
    assert "/static/img/produtos/violetas.jpg" in pagina
    assert "Pedir pelo WhatsApp" in pagina
    assert "Violetas" in pagina


def test_atualizar_estoque_invalido(cliente_admin):
    resposta = cliente_admin.post(
        "/admin/estoque/atualizar/5",
        data={"estoque": "-2"}
    )

    assert resposta.status_code == 400
