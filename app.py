from flask import Flask, render_template
from models import db, Movie, YearlyStats, TopMovies
from jinja2 import Environment
import numpy as np

def intcomma(value):
    return "{:,}".format(value)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///box_office.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

app.jinja_env.filters['intcomma'] = intcomma

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/movies')
def movie_list():
    try:
        movies = Movie.query.order_by(Movie.year).all()
        return render_template('movie_list.html', movies=movies)
    except Exception as e:
        return render_template('error.html', error=str(e))

@app.route('/stats')
def stats():
    try:
        stats = YearlyStats.query.order_by(YearlyStats.year).all()
        return render_template('stats.html', stats=stats)
    except Exception as e:
        return render_template('error.html', error=str(e))

@app.route('/annual_comparison')
def annual_comparison():
    try:
        stats = YearlyStats.query.order_by(YearlyStats.year).all()
        years = [stat.year for stat in stats]
        grosses = [stat.total_gross for stat in stats]
        max_gross = max(grosses)
        min_gross = min(grosses)
        max_year = years[grosses.index(max_gross)]
        min_year = years[grosses.index(min_gross)]
        return render_template('annual_comparison.html', stats=stats, max_year=max_year, max_gross=max_gross, min_year=min_year, min_gross=min_gross)
    except Exception as e:
        return render_template('error.html', error=str(e))

@app.route('/top_movies')
def top_movies():
    try:
        top_movies = TopMovies.query.order_by(TopMovies.year, TopMovies.rank).all()
        return render_template('top_movies.html', top_movies=top_movies)
    except Exception as e:
        return render_template('error.html', error=str(e))

@app.route('/moving_average')
def moving_average():
    try:
        stats = YearlyStats.query.order_by(YearlyStats.year).all()
        years = [stat.year for stat in stats]
        grosses = [stat.total_gross for stat in stats]
        # Calculate 3-year moving average
        moving_avg = []
        for i in range(len(grosses)):
            if i < 1 or i >= len(grosses) - 1:
                moving_avg.append(grosses[i])
            else:
                avg = (grosses[i-1] + grosses[i] + grosses[i+1]) / 3
                moving_avg.append(avg)
        return render_template('moving_average.html', stats=stats, years=years, grosses=grosses, moving_avg=moving_avg)
    except Exception as e:
        return render_template('error.html', error=str(e))

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', error="Page not found"), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('error.html', error="Internal server error"), 500

if __name__ == '__main__':
    app.run(debug=True)