from __future__ import unicode_literals

from django.db import models

class RefillTracker(models.Model):
    refill_count = models.IntegerField(default=0)
    prescription_id = models.IntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now=True)
