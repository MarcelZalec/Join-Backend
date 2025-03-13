from django.db import models
import datetime


class User(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField((""), max_length=254)


class Contacts(models.Model):
    color = models.TextField(max_length=50, default="#1FD7C1")
    name = models.CharField(max_length=50)
    email = models.EmailField((""), max_length=254)
    number = models.CharField(max_length=15)
    
    def __str__(self):
        return f"{self.name}"


class Task(models.Model):
    TASK_CATEGORIES = [
        ("feedback", "Feedback"),
        ("todo", "To Do"),
        ("progress", "In Progress"),
        ("done", "Done"),
    ]

    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("urgent", "Urgent"),
    ]

    TYPE_CHOICES = [
        ("Technical Task", "Technical Task"),
        ("User Story", "User Story"),
    ]

    title = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    assigned = models.ManyToManyField(Contacts, blank=True)
    date = models.DateField(default=datetime.date.today)
    category = models.CharField(
        max_length=20, choices=TASK_CATEGORIES, default="todo")
    priority = models.CharField(
        max_length=20, choices=PRIORITY_CHOICES, default="medium")
    type = models.CharField(
        max_length=20, choices=TYPE_CHOICES, default="User Story")

    class Meta:
        ordering = ['title']

    def __str__(self):
        return f"{self.title}"


class Subtask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="subtasks", null=True, blank=True)
    task_description = models.CharField(max_length=100, blank=True)
    is_tasked_checked = models.BooleanField(default=False)