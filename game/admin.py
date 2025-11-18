from django.contrib import admin
from .models import UserProfile, Exercise


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'current_level', 'total_correct', 'total_attempts', 'get_accuracy', 'updated_at']
    list_filter = ['current_level', 'created_at']
    search_fields = ['user__username']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ['user', 'level', 'number1', 'number2', 'user_answer', 'correct_answer', 'is_correct', 'created_at']
    list_filter = ['level', 'is_correct', 'created_at']
    search_fields = ['user__username']
    readonly_fields = ['created_at']
