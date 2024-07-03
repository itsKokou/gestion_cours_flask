from app import db


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    libelle = db.Column(db.String(20), unique=True, nullable=False)

    # #OneToMany : Role---User
    # users = db.relationship("User", back_populates="role")

    