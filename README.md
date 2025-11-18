# Math Game - Multiplication Table Practice

A Django-based web application for practicing multiplication tables with progressive difficulty levels.

## Features

- **Multiple Users Support**: Each user has their own account and can register/login independently
- **Progressive Levels**: 10 difficulty levels that increase in complexity
  - Level 1: 1-3 × 1-3
  - Level 2: 1-5 × 1-5
  - Level 3: 1-7 × 1-7
  - Levels 4-10: Progressive difficulty up to 1-12 × 1-12
- **Personal Progress Tracking**: Each user advances at their own pace
- **Automatic Level Advancement**: Users advance when they achieve 80% accuracy on 10 questions at their current level
- **Statistics Dashboard**: Track correct answers, total attempts, and accuracy percentage
- **Exercise History**: Review recent exercises with results

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ynonp/math-game.git
cd math-game
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py migrate
```

4. Create a superuser (optional, for admin access):
```bash
python manage.py createsuperuser
```

5. Start the development server:
```bash
python manage.py runserver
```

6. Open your browser and navigate to `http://localhost:8000`

## Usage

1. **Register**: Create a new account or login with an existing one
2. **Play**: Answer multiplication questions to practice
3. **Progress**: View your statistics and recent exercises
4. **Advance**: Complete 10 questions with 80% accuracy to move to the next level

## Admin Panel

Access the Django admin panel at `http://localhost:8000/admin/` to:
- View all user profiles and their progress
- Monitor exercise attempts and results
- Manage users and data

## Technologies Used

- Python 3.12+
- Django 5.2+
- SQLite (default database)
- HTML/CSS (responsive design)