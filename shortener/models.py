from django.db import models


class URLShortener(models.Model):
    origin_url = models.URLField()
    shorten_id = models.CharField(max_length=8)

    def __str__(self):
        return self.shorten_id
