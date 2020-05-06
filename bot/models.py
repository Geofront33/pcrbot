from django.db import models


# Create your models here.
class Card(models.Model):
    cid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    star = models.IntegerField()
    position = models.IntegerField()
    age = models.IntegerField()
    height = models.IntegerField()
    weight = models.IntegerField()

    def __str__(self):
        return self.name + ' ' + '★' * self.star

    def print(self):
        return 'name:  ' + self.name + '\nid:  ' + str(self.cid) + '\nstar:  ' + str(self.star) + '★' \
            + '\nposition:  ' + str(self.position) + '\nage:  ' + str(self.age) + '\nheight:  ' + str(self.height) \
            + '\nweight:  ' + str(self.weight)
