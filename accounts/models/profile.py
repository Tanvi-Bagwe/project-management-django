from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(
        User,
        on_delete=models.DO_NOTHING,
        db_column='user_id'
    )
    phone = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'accounts_profile'

    def __str__(self):
        return self.user.username
