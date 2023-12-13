class Usuario:
    def __init__(self, nome, nickname, senha):
        self.nome = nome
        self.nickname = nickname
        self.senha = senha

usuario1 = Usuario("Lucas Vinícius", "lucas", "lucas123")
usuario2 = Usuario("Elon Mosca", "elmosca", "elmosca123")

usuarios = { usuario1.nickname : usuario1,
             usuario2.nickname : usuario2}