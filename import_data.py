import pandas as pd
from models import db, Movie, YearlyStats, TopMovies
from app import app

# Load the dataset
df = pd.read_csv('movies_2000_2024_clean.csv')
df = df.dropna(subset=['Year', 'Title', 'Gross'])
df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
df['Gross'] = pd.to_numeric(df['Gross'], errors='coerce')
df = df.dropna(subset=['Year', 'Gross'])

with app.app_context():
    db.create_all()

    # Clear existing data
    db.session.query(Movie).delete()
    db.session.query(YearlyStats).delete()
    db.session.query(TopMovies).delete()

    # Insert all movies
    for _, row in df.iterrows():
        movie = Movie(
            year=int(row['Year']),
            title=row['Title'],
            gross=int(row['Gross'])
        )
        db.session.add(movie)

    # Aggregate yearly stats
    yearly_data = df.groupby('Year').agg({'Gross': 'sum', 'Title': 'count'}).reset_index()
    for _, row in yearly_data.iterrows():
        stats = YearlyStats(
            year=int(row['Year']),
            total_gross=int(row['Gross']),
            movie_count=int(row['Title'])
        )
        db.session.add(stats)

    # Insert top 5 movies per year
    for year, group in df.groupby('Year'):
        top_movies = group.sort_values(by='Gross', ascending=False).head(5)
        for rank, (_, row) in enumerate(top_movies.iterrows(), 1):
            top_movie = TopMovies(
                year=int(row['Year']),
                title=row['Title'],
                gross=int(row['Gross']),
                rank=rank
            )
            db.session.add(top_movie)

    db.session.commit()
    print("Data imported successfully!")