from app import db
from .ClasseCours import ClasseCours
from ..models.Module import Module

class Cours(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isArchived = db.Column(db.Boolean, default=False, nullable=False)
    createAt = db.Column(db.Date, nullable=False)
    nbreHeureTotal = db.Column(db.Integer, default= 0)
    nbreHeurePlanifie = db.Column(db.Integer, default= 0)
    nbreHeureRestantPlan = db.Column(db.Integer, default= 0)
    nbreHeureRealise = db.Column(db.Integer, default= 0)

    #ManyToOne : Cours---AnneeScolaire
    anneeScolaire_id = db.Column(db.Integer, db.ForeignKey("annee_scolaire.id"))
    anneeScolaire = db.relationship("AnneeScolaire", backref="cours")

    #ManyToOne : Cours---Semestredb.
    semestre_id = db.Column(db.Integer, db.ForeignKey("semestre.id"))
    semestre = db.relationship("Semestre", backref="cours")

    #ManyToOne : Cours---Module
    module_id = db.Column(db.Integer, db.ForeignKey("module.id"))
    module = db.relationship("Module", backref="cours")

    #ManyToOne : Cours---Professeur
    professeur_id = db.Column(db.Integer, db.ForeignKey("professeur.id"))
    professeur = db.relationship("Professeur", backref="cours")

    # #ManyToMany : Cours---Classe
    classes = db.relationship("Classe", secondary=ClasseCours.__table__, back_populates="cours",  cascade="save-update")

    # #OneToMany : Cours---Seance
    # seances = db.relationship("Seance", back_populates="cours")

    def to_json(self):
        classes = []
        for cl in self.classes :
            classes.append(cl.id)
        return{
            "id": self.id,
            "isArchived": self.isArchived,
            "createAt": self.createAt.strftime("%d-%m-%Y"),
            "nbreHeureTotal": self.nbreHeureTotal,
            "nbreHeurePlanifie": self.nbreHeurePlanifie,
            "nbreHeureRestantPlan": self.nbreHeureRestantPlan,
            "nbreHeureRealise": self.nbreHeureRealise,
            "semestre_id": self.semestre_id,
            "module_id": self.module_id,
            "professeur_id": self.professeur_id,
            "classes": classes
        }
   


