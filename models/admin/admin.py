class Admin:
    def __init__(self, usuario_admin, senha_hash):
        self.usuario_admin = usuario_admin
        self._senha_hash = senha_hash
        