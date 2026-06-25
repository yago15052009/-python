from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .filme import Filme
from .sala import Sala
from .sessao import Sessao
from .ingresso import Ingresso
