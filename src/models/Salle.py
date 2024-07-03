from app import db


class Salle(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isArchived = db.Column(db.Boolean, default=False, nullable=False)
    libelle = db.Column(db.String(20), unique=True, nullable=False)
    nbrePlace = db.Column(db.Integer)

    # #OneToMany : Salle---Seance
    # seances = db.relationship("Seance", back_populates="salle")

    def to_json(self):
        return{
            "id": self.id,
            "isArchived": self.isArchived,
            "libelle": self.libelle,
            "nbrePlace": self.nbrePlace,
        }
