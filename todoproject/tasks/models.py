from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]
    
    title = models.CharField(max_length=225)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateField(null=True, blank=True)
    priority = models.CharField(
        max_length=10, 
        choices=PRIORITY_CHOICES,
        default='Medium'
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='tasks'
    )

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'completed', 'due_date']),
        ]

    def __str__(self):
        return f"{self.title} - {self.user.username}"

    def is_overdue(self):
        from django.utils import timezone
        if self.due_date and not self.completed:
            return self.due_date < timezone.now().date()
        return False