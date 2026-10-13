class Cliente:
    def __init__(self, id, senha_hash, nome, email, telefone):
        self.id = id
        self._senha_hash = senha_hash
        self.nome = nome
        self.email = email
        self.telefone = telefone

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, valor):
        if "@" not in valor:
            raise ValueError("Email inválido.")
        self._email = valor

    def __str__(self):
        return f"Cliente: {self.nome}, Email: {self.email}, Telefone: {self.telefone}"
