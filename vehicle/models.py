from django.db import models

class Vehicle(models.Model):
    VEHICLE_TYPE_CHOICES = (
        ('Two', 'Two Wheeler'),
        ('Three', 'Three Wheeler'),
        ('Four', 'Four Wheeler'),
    )
    vehicle_number = models.CharField(max_length=10)
    vehicle_type = models.CharField(max_length=5, choices=VEHICLE_TYPE_CHOICES)
    vehicle_model = models.CharField(max_length=100)
    vehicle_description = models.TextField()

    def __str__(self):
        return self.vehicle_number
