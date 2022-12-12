from django.db import models


class KeyValueStore(models.Model):
    """
    This Model should be used for all globel key-value pair store.
    Pair should be stored here if we can't keep it in OS variable or in memory.
    """
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.key
