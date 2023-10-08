# color_detector/models.py

from django.db import models


class ColorDetection(models.Model):
    # Define your model fields here
    # Corrected 'upload_to' path
    image = models.ImageField(upload_to='images/')
    colors = models.JSONField()
