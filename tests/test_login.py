
import auth as auth
import app as site
from werkzeug.security import generate_password_hash


def test_acesso_ao_estoque_sem_login_redireciona():
    site.app.config.update(TESTING=True)
    cliente = site.app.test_client()
    resposta = cliente.get('/admin/estoque')
    assert resposta.status_code == 302
    assert '/admin/login' in resposta.headers['Location']


def test_login_invalido(monkeypatch):
    site.app.config.update(TESTING=True)
    monkeypatch.setattr(auth, 'buscar_admin', lambda usuario: None)
    cliente = site.app.test_client()
    resposta = cliente.post('/admin/login', data={'usuario': 'inexistente', 'senha': 'errada'})
    assert resposta.status_code == 200
    assert b'Usu' in resposta.data


def test_login_correto_e_logout(monkeypatch):
    site.app.config.update(TESTING=True)
    hash_senha = generate_password_hash('uma-senha-grande-de-teste')
    monkeypatch.setattr(auth, 'buscar_admin', lambda usuario: (1, 'florista', hash_senha))
    cliente = site.app.test_client()
    resposta = cliente.post('/admin/login', data={'usuario': 'florista', 'senha': 'uma-senha-grande-de-teste'})
    assert resposta.status_code == 302
    assert '/admin/estoque' in resposta.headers['Location']
    with cliente.session_transaction() as sessao:
        assert sessao['admin_usuario'] == 'florista'
    assert cliente.post('/admin/sair').status_code == 302
    assert '/admin/login' in cliente.get('/admin/estoque').headers['Location']
