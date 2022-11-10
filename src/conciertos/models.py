from django.db import models
from django.contrib.auth.models import User

# Create your models hereS.

class TokenUsers(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    spotytoken = models.CharField(max_length=470, null=False)

    def __str__(self):
        return self.user.username