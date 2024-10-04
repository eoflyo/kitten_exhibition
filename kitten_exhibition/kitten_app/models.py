from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from django.db import models
from django.db.models import CASCADE


class Breed(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Kitten(models.Model):
    color = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)
    age = models.IntegerField()
    owner = models.ForeignKey(to=User, related_name='posts', on_delete=models.CASCADE)
    breed = models.ForeignKey(to=Breed, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'Kitten, color:{self.color}, age:{self.age}'


class Rate(models.Model):
    value = models.IntegerField(default=0, validators=[MaxValueValidator(5)])
    author = models.ForeignKey(to=User, on_delete=CASCADE)
    rated_kitten = models.ForeignKey(to=Kitten, on_delete=CASCADE)
