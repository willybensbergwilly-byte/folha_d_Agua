from io import BytesIO
from pathlib import Path
import pytest
from werkzeug.datastructures import FileStorage
from utils.imagens import apagar_imagem, salvar_imagem


def test_imagem_png_salva_e_exclui(tmp_path):
    arquivo = FileStorage(stream=BytesIO(b"\x89PNG\r\n\x1a\n" + b"0" * 20), filename="foto.PNG")
    nome = salvar_imagem(arquivo, tmp_path)
    assert nome.endswith(".png")
    assert (tmp_path / "img" / "produtos" / nome).exists()
    apagar_imagem(nome, tmp_path)
    assert not (tmp_path / "img" / "produtos" / nome).exists()


def test_extensao_invalida(tmp_path):
    arquivo = FileStorage(stream=BytesIO(b"texto"), filename="exec.exe")
    with pytest.raises(ValueError):
        salvar_imagem(arquivo, tmp_path)
