
from django.db import models

class AbstractGlossary(models.Model):
    code = models.CharField(max_length=20)
    label = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)


    class Meta:
        abstract = True
        ordering = ['code']

    def __str__(self):
        return self.label