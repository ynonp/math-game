from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """
    Stores user's progress and level information
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    current_level = models.IntegerField(default=1)
    total_correct = models.IntegerField(default=0)
    total_attempts = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - Level {self.current_level}"
    
    def get_accuracy(self):
        """Calculate user's accuracy percentage"""
        if self.total_attempts == 0:
            return 0
        return (self.total_correct / self.total_attempts) * 100
    
    def advance_level(self):
        """Advance user to the next level"""
        if self.current_level < 10:  # Max level is 10
            self.current_level += 1
            self.save()


class Exercise(models.Model):
    """
    Stores individual exercise attempts
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exercises')
    level = models.IntegerField()
    number1 = models.IntegerField()
    number2 = models.IntegerField()
    user_answer = models.IntegerField(null=True, blank=True)
    correct_answer = models.IntegerField()
    is_correct = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.number1} × {self.number2} = {self.user_answer}"
    
    class Meta:
        ordering = ['-created_at']
