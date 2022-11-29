from django.db import models
# from django.contrib.auth import get_user_model
#
# User = get_user_model()
from useres.models import Coach, Student

class Training(models.Model):
    coach = models.ManyToManyField(Coach, on_delete=models.CASCADE)
    student = models.ManyToManyField(Student, on_delete=models.CASCADE)
    date = models.DateField(blank=True)

    def __str__(self):
        return f'{self.coach.username} at {self.date}'
class Strength_exercise(models.Model):
    title = models.Charfield()
    training_plan = models.ForeignKey(Training,
                                 on_delete=models.SET_NULL)
    numbers_of_sets = models.IntegerField(blank=False)
    rest_time_seconds = models.IntegerField()

class Strength_training_set(models.Model):
    exercise = models.ForeignKey(Strength_exercise,
                                 on_delete=models.SET_NULL)
    numbers_of_repetition = models.IntegerField(blank=False)
    expected_weight = models.DecimalField(max_digits=5,
                                          decimal_places=2,
                                          blank=True)
    actual_weight = models.DecimalField(max_digits=5, decimal_places=2,
                                        blank=False)
    corrections = models.TextField(blank=True)





class TrainingDay(models.Model):
    pass

class Methods(models.Model):
    pass
