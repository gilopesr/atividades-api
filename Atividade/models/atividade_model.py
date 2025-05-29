from database import db
from sqlalchemy.orm import relationship

class Atividade(db.Model):
    __tablename__ = 'atividades'
    id_atividade = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_disciplina = db.Column(db.Integer, nullable=False)
    enunciado = db.Column(db.Text, nullable=False)

    submissoes = relationship('Submissao', backref='atividade', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Atividade {self.id_atividade} - Disciplina {self.id_disciplina}>"

class Submissao(db.Model):
    __tablename__ = 'submissoes'
    id_submissao = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_atividade = db.Column(db.Integer, db.ForeignKey('atividades.id_atividade'), nullable=False)
    id_aluno = db.Column(db.Integer, nullable=False) 
    resposta = db.Column(db.Text, nullable=False) 
    nota = db.Column(db.Integer, nullable=True) 

    def __repr__(self):
        return f"<Submissao {self.id_submissao} - Atv {self.id_atividade} - Aluno {self.id_aluno}>"

