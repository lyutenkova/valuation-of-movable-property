from django.db import models

class ComparativeApproach(CreatedMixin):
    mark = models.CharField(max_length=256, blank=True, null=True)
    country = models.CharField(max_length=256, blank=True, null=True)
    cost_of_new = models.FloatField(null=True, default=None)
    par1_name = models.CharField(max_length=256, blank=True, null=True)
    par1_val = models.FloatField(null=True, default=None)
    par2_name = models.CharField(max_length=256, blank=True, null=True)
    par2_val = models.FloatField(null=True, default=None)

class CostApproach(CreatedMixin):
    year = models.DateField(null=True, default=None)
    mileage = models.FloatField(null=True, default=None)
    offer price = models.FloatField(null=True, default=None)
    par1_name = models.CharField(max_length=256, blank=True, null=True)
    par1_val = models.FloatField(null=True, default=None)
    par2_name = models.CharField(max_length=256, blank=True, null=True)
    par2_val = models.FloatField(null=True, default=None)

