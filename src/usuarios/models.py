from django.db import models

# Create your models here.
class Usuario(models.Model):
    username = models.CharField(max_length=16, primary_key=True, null=False)
    password = models.CharField(max_length=30, null=False)
    
    def __str__(self):
        return self.username