import unittest
from app import app, db
from models import Movie, YearlyStats, TopMovies
from unittest.mock import patch
import os

TEST_DB = 'sqlite:///test_box_office.db'


class FlaskAppTests(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = TEST_DB
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()

        db.create_all()
        self._add_test_data()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def _add_test_data(self):
        # Add more data to test moving average
        movie1 = Movie(year=1995, title="Movie A", gross=1000000)
        movie2 = Movie(year=1996, title="Movie B", gross=1500000)
        movie3 = Movie(year=1997, title="Movie C", gross=1200000)
        yearly_stat1 = YearlyStats(year=1995, total_gross=1000000, movie_count=1)
        yearly_stat2 = YearlyStats(year=1996, total_gross=1500000, movie_count=1)
        yearly_stat3 = YearlyStats(year=1997, total_gross=1200000, movie_count=1)
        top_movie1 = TopMovies(year=1995, title="Movie A", gross=1000000, rank=1)
        top_movie2 = TopMovies(year=1996, title="Movie B", gross=1500000, rank=1)
        top_movie3 = TopMovies(year=1997, title="Movie C", gross=1200000, rank=1)
        db.session.add_all(
            [movie1, movie2, movie3, yearly_stat1, yearly_stat2, yearly_stat3, top_movie1, top_movie2, top_movie3])
        db.session.commit()

    def test_index_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to Box Office Data', response.data)

    def test_index_page_no_data(self):
        db.session.query(Movie).delete()
        db.session.query(YearlyStats).delete()
        db.session.commit()
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_index_page_exception(self):
        with patch('app.Movie.query.count', side_effect=Exception("Database error")):
            response = self.app.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Error', response.data)

    def test_movie_list_default(self):
        response = self.app.get('/movies')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Movie A', response.data)

    def test_movie_list_search(self):
        response = self.app.get('/movies?search=A')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Movie A', response.data)

    def test_movie_list_search_no_results(self):
        response = self.app.get('/movies?search=Nonexistent')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No movies found', response.data)

    def test_movie_list_sort_year_asc(self):
        response = self.app.get('/movies?sort=year_asc')
        self.assertEqual(response.status_code, 200)
        data = response.data.decode('utf-8')
        self.assertTrue(data.index('1995') < data.index('1996'))

    def test_movie_list_sort_year_desc(self):
        response = self.app.get('/movies?sort=year_desc')
        self.assertEqual(response.status_code, 200)
        data = response.data.decode('utf-8')
        self.assertTrue(data.index('1997') < data.index('1995'))

    def test_movie_list_sort_gross_asc(self):
        response = self.app.get('/movies?sort=gross_asc')
        self.assertEqual(response.status_code, 200)
        data = response.data.decode('utf-8')
        self.assertTrue(data.index('1000000') < data.index('1200000'))

    def test_movie_list_sort_gross_desc(self):
        response = self.app.get('/movies?sort=gross_desc')
        self.assertEqual(response.status_code, 200)
        data = response.data.decode('utf-8')
        self.assertTrue(data.index('1500000') < data.index('1000000'))

    def test_movie_list_invalid_sort(self):
        response = self.app.get('/movies?sort=invalid')
        self.assertEqual(response.status_code, 200)
        data = response.data.decode('utf-8')
        self.assertTrue(data.index('1995') < data.index('1996'))

    def test_movie_list_exception(self):
        with patch('app.Movie.query', side_effect=Exception("Database error")):
            response = self.app.get('/movies')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Error', response.data)

    def test_annual_comparison_page(self):
        response = self.app.get('/annual_comparison')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Annual Gross Comparison', response.data)

    def test_annual_comparison_no_data(self):
        db.session.query(YearlyStats).delete()
        db.session.commit()
        response = self.app.get('/annual_comparison')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No data available', response.data)

    def test_annual_comparison_exception(self):
        with patch('app.YearlyStats.query', side_effect=Exception("Database error")):
            response = self.app.get('/annual_comparison')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Error', response.data)

    def test_stats_page(self):
        response = self.app.get('/stats')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Yearly Statistics', response.data)

    def test_stats_exception(self):
        with patch('app.YearlyStats.query', side_effect=Exception("Database error")):
            response = self.app.get('/stats')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Error', response.data)

    def test_top_movies_page(self):
        response = self.app.get('/top_movies')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Movie A', response.data)

    def test_top_movies_exception(self):
        with patch('app.TopMovies.query', side_effect=Exception("Database error")):
            response = self.app.get('/top_movies')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Error', response.data)

    def test_moving_average_page(self):
        response = self.app.get('/moving_average')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Moving Average Analysis', response.data)

    def test_moving_average_no_data(self):
        db.session.query(YearlyStats).delete()
        db.session.commit()
        response = self.app.get('/moving_average')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No data available', response.data)

    def test_moving_average_exception(self):
        with patch('app.YearlyStats.query', side_effect=Exception("Database error")):
            response = self.app.get('/moving_average')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Error', response.data)

    def test_server_error(self):
        # Trigger a 500 error by raising an exception in a route
        with self.app.test_request_context('/'):
            with patch('app.render_template', side_effect=Exception("Template error")):
                response = self.app.get('/')
                self.assertEqual(response.status_code, 500)
                self.assertIn(b'Internal server error', response.data)

    def test_error_handling_404(self):
        response = self.app.get('/nonexistent')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Page not found', response.data)


if __name__ == '__main__':
    unittest.main()