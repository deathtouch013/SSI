from django.db import models

# Create your models here.
class Usuario(models.Model):
    username = models.CharField(max_length=16, primary_key=True, null=False)
    user_hash_id = models.CharField(max_length=64, null=False)
    
    def __str__(self):
        return self.username