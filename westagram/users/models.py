from django.db import models

class Users(models.Model):
    username = models.CharField(max_length=50, null=False, blank=False, unique=True)
    #email = models.EmailField(max_length=300)
    password = models.CharField(max_length=300, null=False, blank=False)

    class Meta:
        db_table = 'user_data'

