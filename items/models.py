from django.db import models
from django.utils.translation import gettext_lazy as _
import re
si_prefix_search = re.compile(r"(?P<prefix>^[pnumkMG]?)(?P<base>[\s\S]{1,}$)")

item_type = [
        ('co', _('Component')),
        ('ap', _('Assembly Part')),
        ('cm', _('Consumable')),
    ]

item_value_units = [
    ('pcs', _('pcs')),
    ('ml', _('ml')),
    ('g', _('g')),
    ('mm', _('mm')),
]


def unit_conversion(source, target, value):
    """
    >>> unit_conversion('km', 'm', 10)
    (10000.0, 'm')

    >>> unit_conversion('m', 'km', 10)
    (0.01, 'km')

    >>> unit_conversion('kHz', 'Hz', 10)
    (10000.0, 'Hz')

    >>> unit_conversion('Hz', 'kHz', 10)
    (0.01, 'kHz')

    >>> unit_conversion('km', 'l', 10)
    Traceback (most recent call last):
        ...
    ValueError

    >>> unit_conversion('kl abbagalamaga', 'kl', 10)
    Traceback (most recent call last):
        ...
    ValueError


    :param source:
    :param target:
    :param value:
    :return:
    """
    si_prefix = {
        'm': 1,
        '': 1000,
        'k': 1000000,
        'M': 1000000000,
    }
    if source == 'pcs' or target == 'pcs':
        return value, 'pcs'
    elif source == target:
        return value, target
    else:
        source_prefix, source_base = si_prefix_search.findall(source)[0]
        target_prefix, target_base = si_prefix_search.findall(target)[0]

        if source_base == target_base:
            ratio = si_prefix[source_prefix] / si_prefix[target_prefix]
            return value*ratio, target
        else:
            raise ValueError()


class Item(models.Model):
    part_number = models.CharField(max_length=200, verbose_name=_('Part Number'), unique=True, null=False, blank=False)
    collection_name = models.CharField(max_length=200, verbose_name=_('Collection name'), null=False, blank=False)
    created_by = models.ForeignKey('auth.User', verbose_name=_('Created_by'), on_delete=models.PROTECT,
                                   null=False, blank=False)
    item_type = models.CharField(max_length=2, verbose_name=_('Type'), choices=item_type,
                                 default='co', null=False, blank=False)
    _price = models.DecimalField(verbose_name='_price', default=0.0, max_digits=10, decimal_places=3,
                                 null=False, blank=False)
    value = models.IntegerField(verbose_name=_('value'), default=0, null=False, blank=False)
    value_units = models.CharField(max_length=5, verbose_name=_('Units'), choices=item_value_units,
                                   default='pcs', null=False, blank=False)
    subcategory = models.ForeignKey('ItemSubCategory', verbose_name=_('Sub Category'), on_delete=models.PROTECT,
                                    null=False, blank=False)
    bom = models.ManyToManyField('self', through='BOM', symmetrical=False, related_name='related_to')

    def __str__(self):
        return self.part_number

    @property
    def price(self):
        if self.item_type != 'ap':
            return self._price
        else:
            return 0.00

    @price.setter
    def price(self, value):
        if self.item_type != 'ap':
            self._price = value


class ItemCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Category name'), unique=True, null=False, blank=False)

    def __str__(self):
        return self.name


class ItemSubCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Sub Category name'), unique=False, null=False, blank=False)
    category = models.ForeignKey('ItemCategory', verbose_name=_('Category'), on_delete=models.PROTECT,
                                 null=False, blank=False)

    def __str__(self):
        return self.name + ' ' + self.category.name


class BOM(models.Model):
    assembly_part = models.ForeignKey('Item', on_delete=models.PROTECT, related_name='assembly_part')
    item = models.ForeignKey('Item', on_delete=models.PROTECT, related_name='used_in')

    # def __str__(self):
    #     return self.assembly_part.part_number + 'BOM'
