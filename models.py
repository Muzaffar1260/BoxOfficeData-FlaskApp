import sqlite3
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    gross = db.Column(db.Integer, nullable=False)

class YearlyStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, unique=True, nullable=False)
    total_gross = db.Column(db.Integer, nullable=False)
    movie_count = db.Column(db.Integer, nullable=False)