from django.contrib.auth.models import User
from django.db import models


class Quote(models.Model):
    text = models.TextField()
    author = models.CharField(max_length=200)
    source = models.CharField(max_length=300, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    is_featured = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['-created_date']
    
    def __str__(self):
        return f'"{self.text}" - {self.author}'
