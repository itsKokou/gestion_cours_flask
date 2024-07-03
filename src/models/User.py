from app import db
from flask_login import UserMixin
from ..models.Role import Role

class User(UserMixin,db.Model):

    id = db.Column(db.Integer ,primary_key=True, autoincrement=True)
    isArchived = db.Column(db.Boolean, default=False, nullable=False)
    login = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    nomComplet = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(20), nullable=False)


    # #ManyToOne : User---Role
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"))
    role =  db.relationship("Role", backref="users")

    #Joined Table Inheritance
    __mapper_args__ = {
        "polymorphic_identity": "USER",
        "polymorphic_on": "type",
    }

