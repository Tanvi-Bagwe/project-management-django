from django.contrib.auth.models import User
from django.db import models


class ProjectStatus(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=30)
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = "project_status"

    def __str__(self):
        return self.name


class Project(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, db_column="created_by")
    status = models.ForeignKey(ProjectStatus, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = "projects"
