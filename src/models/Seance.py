from app import db
from ..models.Salle import Salle


class Seance(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isArchived = db.Column(db.Boolean, default=False, nullable=False)
    isAbsence = db.Column(db.Boolean, default=False, nullable=False)
    codeSeance = db.Column(db.String(20), nullable=True)
    date = db.Column(db.Date, nullable=False)
    heureD = db.Column(db.Time, nullable=False) 
    heureF = db.Column(db.Time, nullable=False)

    #ManyToOne : Seance---Cours
    cours_id = db.Column(db.Integer, db.ForeignKey("cours.id"))
    cours = db.relationship("Cours", backref="seances")

    #ManyToOne : Seance---Salle : Optional
    salle_id = db.Column(db.Integer, db.ForeignKey("salle.id"), nullable=True)
    salle = db.relationship("Salle", backref="seances")

    # #OneToMany : Seance---Absence
    # absences = db.relationship("Absence", back_populates="seance")

    #ManyToOne : Seance---Professeur
    professeur_id = db.Column(db.Integer, db.ForeignKey("professeur.id"), nullable=True)
    professeur = db.relationship("Professeur", backref="seances")

    def to_json(self):
        return{
            "id": self.id,
            "isArchived": self.isArchived,
            "codeSeance": self.codeSeance,
            "date": self.date.strftime("%d-%m-%Y"),
            "heureD": self.heureD.strftime("%H:%M"),
            "heureF": self.heureF.strftime("%H:%M"),
            "cours_id": self.cours_id,
            "salle_id": self.salle_id,
            "professeur_id": self.professeur_id
        }



