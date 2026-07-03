from . import db
from .base import ModeloBase


class Jogador(ModeloBase):
     = "jogadores"



    @property
    def media(self):
        return (self.cabeceio + self.forca) / 2

    @classmethod
    def listar(cls):
        return cls.query.order_by(cls.posicao, cls.nome).all()
