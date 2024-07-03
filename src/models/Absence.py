from app import db



class Absence(db.Model):
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    isArchived = db.Column(db.Boolean,default=False, nullable=False)

    #ManyToOne : Absence---Etudiant
    etudiant_id = db.Column(db.Integer,db.ForeignKey("etudiant.id"))
    etudiant = db.relationship("Etudiant",backref="absences")

    #ManyToOne : Absence---Seance
    seance_id = db.Column(db.Integer, db.ForeignKey("seance.id"))
    seance = db.relationship("Seance",backref="absences")

   


