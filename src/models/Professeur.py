from app import db
from .User import User


class Professeur(User,db.Model):
    id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    portable = db.Column(db.String(20), unique=True, nullable=False)
    grade = db.Column(db.String(20), nullable=False)

    # #OneToMany : Professeur---Cours
    # cours = db.relationship("Cours", back_populates="professeur")

    # #OneToMany : Professeur---Enseignement
    # enseignements = db.relationship("Enseignement", back_populates="professeur")

    # #OneToMany : Professeur---Seance
    # seances = db.relationship("Seance", back_populates="professeur")

    #Joined Table Inheritance
    __mapper_args__ = {
        "polymorphic_identity": "PROFESSEUR",
    }
     
    def to_json(self):
        return{
            "id": self.id,
            "isArchived": self.isArchived,
            "login": self.login,
            "nomComplet": self.nomComplet,
            "portable": self.portable,
            "grade": self.grade
        }


