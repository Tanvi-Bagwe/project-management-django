from django.contrib.auth.models import User
from django.db import models

from projects.models import Project


class TaskStatus(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=30)
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = "task_status"

    def __str__(self):
        return self.name


class TaskPriority(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = "task_priority"

    def __str__(self):
        return self.name


class Task(models.Model):
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING, db_column="project_id")

    title = models.CharField(max_length=200)
    description = models.TextField()

    assigned_to = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name="assigned_tasks", db_column="assigned_to"
    )
    assigned_by = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name="created_tasks", db_column="assigned_by"
    )

    status = models.ForeignKey(TaskStatus, on_delete=models.DO_NOTHING, db_column="status_id")
    priority = models.ForeignKey(TaskPriority, on_delete=models.DO_NOTHING, db_column="priority_id")

    assigned_at = models.DateTimeField()
    due_date = models.DateField(null=True)
    completed_at = models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.title} ({self.project.name})"

    class Meta:
        managed = False
        db_table = "tasks"
        ordering = ['-assigned_at']
