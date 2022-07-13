from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Contato(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    telefone = db.Column(db.String(20), unique=False, nullable=False)
    data_nascimento = db.Column(db.Date, unique=False, nullable=False)
    detalhes = db.Column(db.String, unique=False, nullable=True)
    _deleted = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Contato %r>' % self.nome

    def as_dict(self):
       return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}