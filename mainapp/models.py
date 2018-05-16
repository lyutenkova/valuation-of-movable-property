from django.db import models
from mainapp.mixins import CreateMixin
from datetime import datetime

class ComparativeApproach(CreateMixin):
    name = models.CharField(max_length=256, blank=True, null=True)
    year = models.IntegerField(null=True, default=0)
    mileage = models.FloatField(null=True, default=None)
    offer_price = models.FloatField(null=True, default=None)
    par1_name = models.CharField(max_length=256, blank=True, null=True)
    par1_val = models.FloatField(null=True, default=None)
    par2_name = models.CharField(max_length=256, blank=True, null=True)
    par2_val = models.FloatField(null=True, default=None)

    class Meta:
        db_table = 'comparative_approach'

class CostApproach(CreateMixin):
    mark = models.CharField(max_length=256, blank=True, null=True)
    # country = models.CharField(max_length=256, blank=True, null=True)
    cost_of_new = models.FloatField(null=True, default=None)
    par1_name = models.CharField(max_length=256, blank=True, null=True)
    par1_val = models.FloatField(null=True, default=None)
    par2_name = models.CharField(max_length=256, blank=True, null=True)
    par2_val = models.FloatField(null=True, default=None)

    class Meta:
        db_table = "cost_approach"
