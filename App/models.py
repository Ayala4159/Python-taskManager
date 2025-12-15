from django.db import models

class team(models.Model):
    team_name=models.CharField()

class User(models.Model):
    first_name = models.CharField(max_length=100,),
    last_name = models.CharField(max_length=100),
    email = models.EmailField(),
    role=models.CharField(max_length=100,choices=[('Manager','Manager'),('Team_Member','Team_Member')])
    team=models.ForeignKey(team)


class task(models.Model):