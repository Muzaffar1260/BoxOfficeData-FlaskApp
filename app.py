from flask import Flask, render_template
from models import db, Movie, YearlyStats
from jinja2 import Environment

def intcomma(value):
    return "{:,}".format(value)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///box_office.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Register the Jinja filter
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

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', error="Page not found"), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('error.html', error="Internal server error"), 500

if __name__ == '__main__':
    app.run(debug=True)