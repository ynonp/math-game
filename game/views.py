from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .models import UserProfile, Exercise
import random


def home(request):
    """Home page view"""
    return render(request, 'game/home.html')


def register(request):
    """User registration view"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create user profile
            UserProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('game')
    else:
        form = UserCreationForm()
    return render(request, 'game/register.html', {'form': form})


def user_login(request):
    """User login view"""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('game')
    else:
        form = AuthenticationForm()
    return render(request, 'game/login.html', {'form': form})


def user_logout(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')


@login_required
def game(request):
    """Main game view"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        # Process answer
        exercise_id = request.POST.get('exercise_id')
        user_answer = request.POST.get('answer')
        
        if exercise_id and user_answer:
            try:
                exercise = Exercise.objects.get(id=exercise_id, user=request.user)
                exercise.user_answer = int(user_answer)
                exercise.is_correct = (exercise.user_answer == exercise.correct_answer)
                exercise.save()
                
                # Update profile stats
                profile.total_attempts += 1
                if exercise.is_correct:
                    profile.total_correct += 1
                    messages.success(request, 'Correct! Well done!')
                else:
                    messages.error(request, f'Incorrect. The answer was {exercise.correct_answer}.')
                
                # Check if user should advance to next level
                # Advance if accuracy >= 80% and at least 10 questions answered at current level
                recent_exercises = Exercise.objects.filter(
                    user=request.user, 
                    level=profile.current_level
                ).order_by('-created_at')[:10]
                
                if len(recent_exercises) >= 10:
                    correct_count = sum(1 for e in recent_exercises if e.is_correct)
                    if correct_count >= 8:  # 80% accuracy
                        profile.advance_level()
                        messages.success(request, f'Congratulations! You advanced to level {profile.current_level}!')
                
                profile.save()
                return redirect('game')
            except (Exercise.DoesNotExist, ValueError):
                messages.error(request, 'Invalid submission.')
    
    # Generate new exercise based on level
    exercise = generate_exercise(request.user, profile.current_level)
    
    context = {
        'profile': profile,
        'exercise': exercise,
        'accuracy': profile.get_accuracy(),
    }
    return render(request, 'game/game.html', context)


@login_required
def progress(request):
    """View user's progress and statistics"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    recent_exercises = Exercise.objects.filter(user=request.user).order_by('-created_at')[:20]
    
    context = {
        'profile': profile,
        'recent_exercises': recent_exercises,
        'accuracy': profile.get_accuracy(),
    }
    return render(request, 'game/progress.html', context)



def generate_exercise(user, level):
    """
    Generate a multiplication exercise based on the user's level
    Level 1: 1-3 × 1-3
    Level 2: 1-5 × 1-5
    Level 3: 1-7 × 1-7
    Level 4-10: Progressive difficulty up to 1-12 × 1-12
    """
    if level == 1:
        max_num = 3
    elif level == 2:
        max_num = 5
    elif level == 3:
        max_num = 7
    elif level == 4:
        max_num = 8
    elif level == 5:
        max_num = 9
    elif level == 6:
        max_num = 10
    elif level == 7:
        max_num = 11
    else:  # Level 8-10
        max_num = 12
    
    number1 = random.randint(1, max_num)
    number2 = random.randint(1, max_num)
    correct_answer = number1 * number2
    
    exercise = Exercise.objects.create(
        user=user,
        level=level,
        number1=number1,
        number2=number2,
        correct_answer=correct_answer
    )
    
    return exercise
