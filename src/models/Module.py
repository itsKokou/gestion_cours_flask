from app import db
from .EnseignementModule import EnseignementModule
from ..models.Enseignement import Enseignement


class Module(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isArchived = db.Column(db.Boolean, default=False, nullable=False)
    libelle = db.Column(db.String(50), unique=True, nullable=False)
    
    # #OneToMany : Module---Cours
    # cours = db.relationship("Cours", back_populates="module")

    #ManyToMany : Module---Cours
    enseignements = db.relationship("Enseignement", secondary=EnseignementModule.__table__, back_populates="modules")
