from django.db import models


class GeneratedUrls(models.Model):
    origin_url = models.URLField(unique=True)
    alias_url = models.CharField(max_length=60, db_index=True, unique=True)
    ip_user = models.CharField(max_length=30)
    visited = models.IntegerField(default=0)

    class Meta:
        ordering = ['origin_url']
