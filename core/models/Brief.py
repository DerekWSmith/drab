from django.db import models
from core.models.Item import Item

class Brief(Item):
    summary = models.CharField(max_length=255)

    class Meta:
        db_table = 'ItemBriefs'