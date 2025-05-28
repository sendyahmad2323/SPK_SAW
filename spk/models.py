from django.db import models
from django.contrib.auth.models import User

class Criteria(models.Model):
    ATTRIBUTE_CHOICES = (
        ('benefit', 'Benefit'),
        ('cost', 'Cost'),
    )

    name = models.CharField(max_length=100, unique=True)
    weight = models.FloatField(default=0)
    attribute = models.CharField(max_length=10, choices=ATTRIBUTE_CHOICES)

    def __str__(self):
        return self.name


class Framework(models.Model):
    name = models.CharField(max_length=100)
    performa = models.IntegerField()
    skalabilitas = models.IntegerField()
    komunitas = models.IntegerField()
    kemudahan_belajar = models.IntegerField()
    pemeliharaan = models.IntegerField()

    def __str__(self):
        return self.name


class FrameworkScore(models.Model):
    framework = models.ForeignKey(Framework, on_delete=models.CASCADE)
    criteria = models.ForeignKey(Criteria, on_delete=models.CASCADE)
    value = models.FloatField(default=0)

    class Meta:
        unique_together = ('framework', 'criteria')

    def __str__(self):
        return f"{self.framework.name} - {self.criteria.name}: {self.value}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preferences = models.JSONField(default=dict)

    def __str__(self):
        return self.user.username