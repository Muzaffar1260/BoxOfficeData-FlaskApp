import pandas as pd
from models import db, Movie, YearlyStats
from app import app

# Load the dataset
df = pd.read_csv('movies_1995_2008_clean.csv')

# Initialize Flask app context
with app.app_context():
    db.create_all()  # Create tables

    # Clear existing data
    db.session.query(Movie).delete()
    db.session.query(YearlyStats).delete()

    # Insert movies
    for _, row in df.iterrows():
        movie = Movie(
            year=row['Year'],
            title=row['Title'],
            gross=row['Gross']
        )
        db.session.add(movie)

    # Aggregate stats by year
    yearly_data = df.groupby('Year').agg({'Gross': 'sum', 'Title': 'count'}).reset_index()
    for _, row in yearly_data.iterrows():
        stats = YearlyStats(
            year=row['Year'],
            total_gross=row['Gross'],
            movie_count=row['Title']
        )
        db.session.add(stats)

    db.session.commit()
    print("Data imported successfully!")