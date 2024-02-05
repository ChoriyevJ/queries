from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    title = models.CharField(max_length=255)
    objects = models.Manager()

    class Meta:
        abstract = True


class Region(BaseModel):
    pass

    def __str__(self):
        return self.title


class District(BaseModel):
    region = models.ForeignKey(Region, on_delete=models.CASCADE,
                               related_name='districts')

    def __str__(self):
        return f'{self.title}-{self.region}'


class School(BaseModel):
    district = models.ForeignKey(District, on_delete=models.CASCADE,
                                 related_name='schools')

    def __str__(self):
        return f'{self.title}-{self.district}'

    class Meta:
        unique_together = ('district', 'title')


class Pupil(models.Model):
    full_name = models.CharField(max_length=255, unique=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE,
                               related_name='pupils')
    objects = models.Manager()
    
    def __str__(self):
        return f'{self.full_name}-{self.school}'


class Test(models.Model):
    total_answers = models.IntegerField()
    correct_answers = models.IntegerField()
    percent = models.DecimalField(default=0, decimal_places=2,
                                  max_digits=5)
    date = models.DateField(default=timezone.now)
    pupil = models.ForeignKey(Pupil, on_delete=models.CASCADE,
                              related_name='tests')
    objects = models.Manager()

    def save(self, *args, **kwargs):
        self.percent = self.correct_answers / self.total_answers * 100
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.pupil}'
