from django.db import models
from django.conf import settings
from job.models import Job


class Application(models.Model):

    STATUS_CHOICES = (
        ('pending','Pending'),
        ('accepted','Accepted'),
        ('rejected','Rejected')
    )

    job = models.ForeignKey(Job, on_delete=models.CASCADE,related_name='applications')
    candidate = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name = 'applications')
    cover_letter = models.TextField()
    resume = models.FileField(upload_to='resumes/',null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('job','candidate')
    
    def __str__(self):
        return f"{self.candidate.username}-{self.job.title}"