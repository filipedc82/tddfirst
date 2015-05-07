from django.db import models

class Product(models.Model):
    PRODUCT_GROUPS = (
        ('VG', 'Valve Guide'),
        ('VS', 'Valve Seat'),
        ('EV', 'Engine Valve'),
        ('EVO', 'Engine Valve Other'),
        ('NGP', '(Normalien)Guide Pin'),
        ('NLS', '(Normalien)Limit Switch'),
        ('NLS', '(Normalien)Other'),
        ('O', 'Other'),
    )
    product_group = models.CharField(max_length=50, choices=PRODUCT_GROUPS, default="O")
    own_product_no = models.CharField(max_length=50)

    def __str__(self):
        return str(self.own_product_no)
