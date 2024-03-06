from django.db import models

class Task(models.Model):
    Task_STATUS =[
        ('pending','pending'),
        ('completed','completed'),
        ('in_progress','in_progress')
    ]

    task_id=models.IntegerField()
    task_name = models.CharField(max_length=40)
    task_discriptions=models.TextField()
    task_status = models.CharField(max_length=45, choices = Task_STATUS)
    task_assigned_by=models.ForeignKey("auth_app.User",on_delete=models.CASCADE,related_name='user_task')
    task_assigned_to = models.ForeignKey("auth_app.User",on_delete=models.CASCADE,related_name='tasks')
    task_assigned_date=models.DateTimeField(auto_now_add=True)
    task_completed_date =models.DateTimeField(blank=True,null =True)
    task_deadline = models.DateTimeField(blank=True,null=True)