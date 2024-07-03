from app import db



class Niveau(db.Model):
    id  = db.Column(db.Integer, primary_key=True, autoincrement=True)
    libelle  = db.Column(db.String(20), unique=True, nullable=False)
    
    # #OneToMany : Niveau---Classe
    # classes = db.relationship("Classe", back_populates="niveau")

    # #OneToMany : Niveau---Semestre
    # semestres = db.relationship("Semestre", back_populates="niveau")

    def to_json(self):
        return{
            "id": self.id,
            "libelle": self.libelle
        }