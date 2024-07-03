from app import db
from .ClasseCours import ClasseCours



class Classe(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isArchived = db.Column(db.Boolean, default=False, nullable=False)
    libelle = db.Column(db.String(20), unique=True, nullable=False)
    effectif = db.Column(db.Integer)

    #ManyToOne : Classe---Niveau
    niveau_id  = db.Column(db.Integer, db.ForeignKey("niveau.id"))
    niveau = db.relationship("Niveau", backref="classes")

    #ManyToOne : Classe---Filiere
    filiere_id = db.Column(db.Integer, db.ForeignKey("filiere.id"))
    filiere = db.relationship("Filiere", backref="classes")

    # #OneToMany : Classe---Inscription
    # inscriptions = db.relationship("Inscription", back_populates="classe")

    # #OneToMany : Classe---Enseignement
    # enseignements = db.relationship("Enseignement", back_populates="classe")

    #ManyToMany : Classe---Cours
    cours = db.relationship("Cours", secondary=ClasseCours.__table__, back_populates="classes")

    def to_json(self):
        return{
            "id": self.id,
            "isArchived": self.isArchived,
            "libelle": self.libelle,
            "effectif": self.effectif,
            "niveau_id": self.niveau_id,
            "filiere_id": self.filiere_id
        }
