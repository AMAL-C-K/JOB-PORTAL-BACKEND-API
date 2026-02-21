from django.db import models
from django.conf import settings


class Job(models.Model):
    
    JOB_TYPE_CHOICES = (
        ('full_time','Full Time'),
        ('part_time', 'Part Time'),
        ('internship', 'Internship')
    )

    employer = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title