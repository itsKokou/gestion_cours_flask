from app import db
from .User import User


class Etudiant(User,db.Model):
    id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    matricule = db.Column(db.String(20), unique=True, nullable=False)
    tuteur = db.Column(db.String(50), nullable=False)
    photo = db.Column(db.String(50), unique=True, nullable=False)

    # #OneToMany : Etudiant---Inscription
    # inscriptions = db.relationship("Inscription", back_populates="etudiant")

    # #OneToMany : Etudiant---Absence
    # absences = db.relationship("Absence", back_populates="etudiant")

    #Joined Table Inheritance
    __mapper_args__ = {
        "polymorphic_identity": "ETUDIANT",
    }

    


