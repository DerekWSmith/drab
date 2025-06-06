import uuid
from django.db import models

class AbstractGlossary(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True)
    code = models.CharField(max_length=20)
    label = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)


    class Meta:
        abstract = True
        ordering = ['code']

    def __str__(self):
        return self.label