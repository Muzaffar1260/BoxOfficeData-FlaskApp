import pandas as pd
from models import db, Movie, YearlyStats
from app import app

# Load the dataset
df = pd.read_csv('movies_1995_2008_clean.csv')

# Clean the dataset: remove rows with NaN in any column
df = df.dropna(subset=['Year', 'Title', 'Gross'])

# Ensure 'Year' and 'Gross' are numeric
df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
df['Gross'] = pd.to_numeric(df['Gross'], errors='coerce')

# Remove any remaining rows where Year or Gross are NaN after conversion
df = df.dropna(subset=['Year', 'Gross'])

# Initialize Flask app context
with app.app_context():
    db.create_all()  # Create tables

    # Clear existing data
    db.session.query(Movie).delete()
    db.session.query(YearlyStats).delete()

    # Insert movies
    for _, row in df.iterrows():
        movie = Movie(
            year=int(row['Year']),  # Ensure year is an integer
            title=row['Title'],
            gross=int(row['Gross'])  # Ensure gross is an integer
        )
        db.session.add(movie)

    # Aggregate stats by year
    yearly_data = df.groupby('Year').agg({'Gross': 'sum', 'Title': 'count'}).reset_index()
    for _, row in yearly_data.iterrows():
        stats = YearlyStats(
            year=int(row['Year']),
            total_gross=int(row['Gross']),
            movie_count=int(row['Title'])
        )
        db.session.add(stats)

    db.session.commit()
    print("Data imported successfully!")