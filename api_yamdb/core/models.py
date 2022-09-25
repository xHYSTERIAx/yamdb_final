from django.db import models
from django.utils import timezone


class CreatedModel(models.Model):
    """Abstract model. Adding date of creation."""
    pub_date = models.DateTimeField(
        'Дата создания',
        default=timezone.now
    )

    class Meta:
        abstract = True
