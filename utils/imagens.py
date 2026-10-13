"""Funções reutilizáveis para salvar/remover imagens de produtos."""
from pathlib import Path
from uuid import uuid4
from werkzeug.utils import secure_filename

EXTENSOES = {".jpg", ".jpeg", ".png", ".webp"}


def salvar_imagem(arquivo, pasta_static):
    """Retorna o nome do arquivo salvo, ou None quando não há novo upload."""
    if not arquivo or not arquivo.filename:
        return None

    extensao = Path(secure_filename(arquivo.filename)).suffix.lower()
    if extensao not in EXTENSOES:
        raise ValueError("Formato inválido. Envie JPG, PNG ou WEBP.")

    # Verificação básica de assinatura, além da extensão do arquivo.
    inicio = arquivo.stream.read(16)
    arquivo.stream.seek(0)
    formatos = {
        ".jpg": inicio.startswith(b"\xff\xd8\xff"),
        ".jpeg": inicio.startswith(b"\xff\xd8\xff"),
        ".png": inicio.startswith(b"\x89PNG\r\n\x1a\n"),
        ".webp": inicio.startswith(b"RIFF") and inicio[8:12] == b"WEBP",
    }
    if not formatos[extensao]:
        raise ValueError("O arquivo não parece ser uma imagem válida.")

    pasta = Path(pasta_static) / "img" / "produtos"
    pasta.mkdir(parents=True, exist_ok=True)
    nome = f"{uuid4().hex}{extensao}"
    arquivo.save(pasta / nome)
    return nome


def apagar_imagem(nome, pasta_static):
    """Remove apenas arquivos locais da pasta de imagens dos produtos."""
    if nome and Path(nome).name == nome:
        arquivo = Path(pasta_static) / "img" / "produtos" / nome
        arquivo.unlink(missing_ok=True)
