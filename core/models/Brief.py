import uuid
from django.db import models
from core.models.Item import Item

class Brief(Item):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    summary = models.CharField(max_length=255)

    class Meta:
        db_table = 'ItemBriefs'