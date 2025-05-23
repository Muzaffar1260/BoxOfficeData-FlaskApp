# BoxOfficeData-FlaskApp

## Overview
**BoxOfficeData-FlaskApp** is a Flask-based web application designed to analyze box office data from 2000 to 2024. The app provides interactive visualizations, including annual gross comparisons with bar charts, a 3-year moving average analysis with line charts, and top-grossing movies displayed in yearly tables. Users can explore a searchable and sortable movie list, view yearly statistics, and navigate a styled interface featuring a gradient banner and stat cards on the homepage. The project includes comprehensive testing (90%+ coverage) and is deployable using SQLite.

### Design
- **Models**:
  - `Movie`: Stores movie details (year, title, gross).
  - `YearlyStats`: Aggregates yearly data (year, total_gross, movie_count).
  - `TopMovies`: Tracks top-grossing movies by year (year, title, gross, rank).
- **Dataset**: Updated to cover 2000–2024, stored in `box_office.db` (SQLite), with data accessible at [https://github.com/Muzaffar1260/BoxOfficeData-FlaskApp](https://github.com/Muzaffar1260/BoxOfficeData-FlaskApp).
- **Architecture**: Follows Flask’s lightweight structure with Jinja2 templates for rendering, Chart.js for visualizations, and custom CSS for styling.

### Dataset Update
The dataset was sourced from [https://www.kaggle.com/datasets/harios/box-office-data-1984-to-2024-from-boxofficemojo](https://www.kaggle.com/datasets/harios/box-office-data-1984-to-2024-from-boxofficemojo), originally covering 1984 to 2024. It was shortened to focus on 2000–2024:
- **Data Source**: Kaggle dataset providing comprehensive box office data.
- **Update Process**: Filtered and imported data into `box_office.db` using SQLAlchemy, focusing on the 2000–2024 range, with updates to `Movie`, `YearlyStats`, and `TopMovies` tables.
- **Validation**: Ensured data integrity by removing duplicates and verifying non-negative gross values.
- **Result**: The refined dataset includes movies from 2000 to 2024, offering a focused view of recent box office trends.

### Development
- **Tools**: Developed using Pycharm Community Edition and tested on Codio as well, Python 3, Flask, and SQLAlchemy.
- **Challenges**:
  - Handled database exceptions to prevent crashes on empty or malformed data.
  - Integrated Chart.js for dynamic visualizations (bar and line charts).
  - Achieved high test coverage by simulating edge cases like database failures.
- **Testing**: Used `unittest` and `coverage.py` to ensure robustness.

### Implementation
- **Features**:
  - Homepage with the title "BoxOfficeData-FlaskApp" and stat cards (total movies, total gross, highest-grossing year).
  - Searchable and sortable movie list (`/movies`).
  - Annual gross comparison with bar charts (`/annual_comparison`).
  - 3-year moving average analysis with line charts (`/moving_average`).
  - Top movies by year with tables (`/top_movies`).
- **Styling**: Custom CSS, card-based layouts, and responsive design.
- **Database**: SQLite (`box_office.db`) with SQLAlchemy for ORM.
- **Error Handling**: Includes 404 and 500 error pages for better user experience.

## Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Muzaffar1260/BoxOfficeData-FlaskApp.git
   cd BoxOfficeData-FlaskApp
