from django.db import models
from django.core.urlresolvers import reverse

class Order(models.Model):
    order_no = models.TextField(max_length=50)
    customer = models.TextField(max_length=50)

    def __str__(self):
        return self.order_no

    def get_absolute_url(self):
        return reverse('order_detail', kwargs={'pk': self.pk})