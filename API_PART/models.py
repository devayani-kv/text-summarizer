from django.db import models

# Create your models here.
class data(models.Model):
    choices_ = (
        ('Extractive','Extractive'),
        ('Abstractive', 'Abstractive')
    )
    link = models.CharField(max_length = 1000)
    inputtext = models.CharField(max_length = 1000)
    option = models.CharField(max_length = 30, choices = choices_)

    def __str__(self):
        return self.inputtext, self.option 