from django.db import models
from django.utils.translation import gettext_lazy as _

item_type = [
        ('co', _('Component')),
        ('ap', _('Assembly Part')),
        ('cm', _('Consumables')),
    ]

item_value_units = [
    ('pcs', _('pcs')),
    ('ml', _('ml')),
    ('g', _('g')),
    ('mm', _('mm')),
]


def unit_conversion(source, target, value):
    '''

    >>> unit_conversion('km', 'm', 10)
    10000

    :param source:
    :param target:
    :param value:
    :return:
    '''
    si_prefix = {
        'm': 1,
        ' ': 1000,
        'k': 1000000,
        'M': 1000000000,
    }
    if source == 'pcs' or target == 'pcs':
        return value, 'pcs'
    elif source == target:
        return value, target
    else:
        source_prefix = ' '
        source_base = ''
        target_prefix = ' '
        target_base = ''
        if len(source) == 1:
            source_prefix = ' '
            source_base = source
        else:
            source_prefix = source[0]
            source_base = source[1:]

        if len(target) == 1:
            target_prefix = ' '
            target_base = target
        else:
            target_prefix = target[0]
            target_base = target[1:]

        if source_base == target_base:
            ratio = si_prefix[target_prefix] / si_prefix[source_prefix]
            return value*ratio, target
        else:
            raise ValueError()


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

