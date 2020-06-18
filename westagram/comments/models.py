from django.db import models
from users.models import Users

class Comments(models.Model):
    username = models.ForeignKey(Users, on_delete = models.CASCADE)
    comment = models.CharField(max_length=1000, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = 'comments_list'
