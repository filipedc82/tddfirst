from django.db import models

class Order(models.Model):
    order_no = models.TextField()
    customer = models.TextField()

    def __str__(self):
        return self.order_no