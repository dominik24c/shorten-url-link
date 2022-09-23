from django.db import models


class GeneratedUrls(models.Model):
    origin_url = models.URLField(unique=True, db_index=True)
    alias_url = models.CharField(max_length=60, unique=True)

    class Meta:
        ordering = ['origin_url']
