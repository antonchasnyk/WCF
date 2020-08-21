from django.db import models
from django.utils.translation import gettext_lazy as _

item_type = [
        ('co', _('Component')),
        ('ap', _('Assembly Part')),
        ('cm', _('Consumables')),
    ]

item_value_units = [
    ('pcs', _('pcs')),
    ('l', _('l')),
    ('kg', _('kg')),
    ('m', _('m')),
]


class Item(models.Model):
    part_number = models.CharField(max_length=200, verbose_name=_('Part Number'), unique=True, null=False, blank=False)
    collection_name = models.CharField(max_length=200, verbose_name=_('Collection name'), null=False, blank=False)
    created_by = models.ForeignKey('User', verbose_name=_('Created_by'), on_delete=models.PROTECT,
                                   null=False, blank=False)
    item_type = models.CharField(max_length=2, verbose_name=_('Type'), choices=item_type,
                                 default='co', null=False, blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    value = models.IntegerField(verbose_name=_('value'), default=0, null=False, blank=False)
    value_units = models.CharField(max_length=5, verbose_name=_('Units'), choices=item_value_units,
                                   default='pcs', null=False, blank=False)
