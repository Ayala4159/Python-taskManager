from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator


class Team(models.Model):
    team_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.team_name


class User(models.Model):
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=20, validators=[MinLengthValidator(8)])
    role = models.CharField(max_length=20, choices=[('Manager', 'Manager'), ('Team_Member', 'Team_Member')], null=True)
    team = models.ForeignKey("Team", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


def start_date_validation(value):
    if value < timezone.now().date():
        raise ValidationError("The date cannot be in the past.")


def end_date_validation(value):
    if value <= timezone.now().date():
        raise ValidationError("Please enter a future date")


class Task(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField(validators=[start_date_validation])
    end_date = models.DateField(validators=[end_date_validation])
    status = models.CharField(max_length=100, choices=[('NEW', 'NEW'),
                                       ('IN_PROGRESS', 'IN_PROGRESS'), ('DONE', 'DONE')], null=True, default='NEW')
    team = models.ForeignKey("Team", on_delete=models.CASCADE)
    owner = models.ForeignKey("User", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.name} : {self.status}"

    def clean(self):
        if self.start_date and self.end_date:
            if self.start_date > self.end_date:
                raise ValidationError("End date cannot be earlier than start date.")
