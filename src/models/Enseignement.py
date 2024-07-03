from app import db
from .EnseignementModule import EnseignementModule
from ..models.Professeur import Professeur

class Enseignement(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    #ManyToOne : Enseignement---AnneeScolaire
    anneeScolaire_id = db.Column(db.Integer, db.ForeignKey("annee_scolaire.id"))
    anneeScolaire = db.relationship("AnneeScolaire", backref="enseignements")

    #ManyToOne : Enseignement---Professeur
    professeur_id = db.Column(db.Integer, db.ForeignKey("professeur.id"))
    professeur = db.relationship("Professeur", backref="enseignements")

    #ManyToOne : Enseignement---Classe
    classe_id = db.Column(db.Integer, db.ForeignKey("classe.id"))
    classe = db.relationship("Classe", backref="enseignements")

    #ManyToMany : Enseignement---Module
    modules = db.relationship("Module", secondary=EnseignementModule.__table__, back_populates="enseignements")

    def to_json(self):
        mods = []
        for mod in self.modules :
            mods.append(mod.id)
        return{
            "id": self.id,
            "anneeScolaire_id": self.anneeScolaire_id,
            "professeur_id": self.professeur_id,
            "classe_id": self.classe_id,
            "modules": mods,
        }
