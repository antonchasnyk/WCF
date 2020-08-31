from django.db import models

# Create your models here.


class ItemPrice(models.Model):
    item = models.ForeignKey('items.Item', on_delete=models.CASCADE, null=False, blank=False)
    price = models.DecimalField(verbose_name='price', default=0.0, max_digits=10, decimal_places=3,
                                 null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return str(self.item) + ' ' + str(self.created_at)