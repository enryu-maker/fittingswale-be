from django.db import models

# Create your models here.

class PrivacyPolicy(models.Model):
    section = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return self.section
    
class TermsAndCondition(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    
    def __str__(self):
        return self.title

class RefundCancellationPolicy(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    
    def __str__(self):
        return self.title
