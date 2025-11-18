from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import UserProfile, Exercise


class UserProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.profile = UserProfile.objects.create(user=self.user)

    def test_profile_creation(self):
        """Test that a user profile is created correctly"""
        self.assertEqual(self.profile.current_level, 1)
        self.assertEqual(self.profile.total_correct, 0)
        self.assertEqual(self.profile.total_attempts, 0)

    def test_get_accuracy(self):
        """Test accuracy calculation"""
        self.assertEqual(self.profile.get_accuracy(), 0)
        
        self.profile.total_attempts = 10
        self.profile.total_correct = 8
        self.assertEqual(self.profile.get_accuracy(), 80.0)

    def test_advance_level(self):
        """Test level advancement"""
        initial_level = self.profile.current_level
        self.profile.advance_level()
        self.assertEqual(self.profile.current_level, initial_level + 1)


class ExerciseModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_exercise_creation(self):
        """Test that an exercise is created correctly"""
        exercise = Exercise.objects.create(
            user=self.user,
            level=1,
            number1=2,
            number2=3,
            correct_answer=6
        )
        self.assertEqual(exercise.number1, 2)
        self.assertEqual(exercise.number2, 3)
        self.assertEqual(exercise.correct_answer, 6)
        self.assertFalse(exercise.is_correct)


class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_home_view(self):
        """Test home page loads successfully"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Multiplication Table Game')

    def test_register_view(self):
        """Test user registration"""
        response = self.client.post('/register/', {
            'username': 'newuser',
            'password1': 'testpass123',
            'password2': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login_view(self):
        """Test user login"""
        response = self.client.post('/login/', {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful login

    def test_game_view_requires_login(self):
        """Test that game view requires authentication"""
        response = self.client.get('/game/')
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_game_view_authenticated(self):
        """Test game view for authenticated users"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/game/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Level')

    def test_progress_view_authenticated(self):
        """Test progress view for authenticated users"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/progress/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Your Progress')
