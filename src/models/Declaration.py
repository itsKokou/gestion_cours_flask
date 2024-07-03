from app import db



class Declaration(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    motif = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)

    #ManyToOne : Declaration---User
    user_id  = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", backref="declarations")

    #ManyToOne : Declaration---Seance
    seance_id = db.Column(db.Integer, db.ForeignKey("seance.id"))
    seance = db.relationship("Seance", backref="declarations")
    
    