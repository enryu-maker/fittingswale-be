from django.db import models

class PrivacyPolicy(models.Model):
    section = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return self.section
    
class RefundCancellationPolicy(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    
    def __str__(self):
        return self.title
    
class TermsAndCondition(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    
    def __str__(self):
        return self.title

class Banner(models.Model):
    image = models.ImageField(upload_to="banner")