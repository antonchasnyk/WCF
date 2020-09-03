from django.db import models
from django.db.models import Sum
from django.urls import reverse_lazy, reverse
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
        'p': 10E-12,
        'n': 10E-9,
        'u': 10E-6,
        'm': 10E-3,
        '': 1,
        'k': 10E3,
        'M': 10E6,
        'G': 10E9,
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


class ValuedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().annotate(value=Sum('item_value__value'))


class ComponentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().annotate(value=Sum('item_value__value')).filter(item_type='co')


class AssemblyPartsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().annotate(value=Sum('item_value__value')).filter(item_type='ap')


class ConsumableManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().annotate(value=Sum('item_value__value')).filter(item_type='cm')


class Item(models.Model):
    part_number = models.CharField(max_length=200, verbose_name=_('Part Number'), unique=True,
                                   null=False, blank=False)
    comment = models.CharField(max_length=200, default='', verbose_name=_('Comment'),
                               unique=False, null=True, blank=True)
    created_by = models.ForeignKey('auth.User', verbose_name=_('Created_by'), on_delete=models.PROTECT,
                                   null=False, blank=False)
    item_type = models.CharField(max_length=2, verbose_name=_('Type'), choices=item_type,
                                 default='co', null=False, blank=False)
    value_units = models.CharField(max_length=5, verbose_name=_('Units'), choices=item_value_units,
                                   default='pcs', null=False, blank=False)
    subcategory = models.ForeignKey('ItemSubCategory', verbose_name=_('Category'), on_delete=models.PROTECT,
                                    null=False, blank=False)
    attributes = models.JSONField(verbose_name=_('Attributes'), null=True, blank=True)
    bom = models.ManyToManyField('self', through='BOM', symmetrical=False, related_name='related_to')

    objects = models.Manager()
    valued_objects = ValuedManager()
    components = ComponentManager()
    assembly_parts = AssemblyPartsManager()
    consumable = ConsumableManager()

    def __str__(self):
        return self.part_number

    def get_value(self):
        return self.item_value.aggregate(value=Sum('value'))['value']

    def designator(self):
        return self.comment + ' ' + self.part_number if self.comment else self.part_number

    def get_absolute_url(self):
        if self.item_type == 'co':
            return reverse_lazy('items:detail_component', kwargs={'component_id': self.pk})
        elif self.item_type == 'ap':
            return "/" + str(self.pk)
        elif self.item_type == 'cm':
            return "/" + str(self.pk)

    def get_edit_url(self):
        if self.item_type == 'co':
            return "/" + self.pk
        elif self.item_type == 'ap':
            return "/" + self.pk
        elif self.item_type == 'cm':
            return "/" + self.pk


class ItemCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Category name'), unique=True, null=False, blank=False)

    def __str__(self):
        return self.name


class ItemSubCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Sub Category name'), unique=False,
                            null=False, blank=False)
    category = models.ForeignKey('ItemCategory', verbose_name=_('Category'), on_delete=models.PROTECT,
                                 null=False, blank=False)

    def __str__(self):
        return self.name + ' ' + self.category.name


class BOM(models.Model):
    item = models.ForeignKey('Item', on_delete=models.PROTECT, related_name='used_in')
    assembly_part = models.ForeignKey('Item', on_delete=models.CASCADE, related_name='consist_of')
    position = models.CharField(max_length=200, verbose_name=_('position'),
                                unique=False, null=False, blank=False)
    quantity = models.IntegerField(default=0, verbose_name=_('Quantity'), null=False, blank=False)

    def __str__(self):
        return self.assembly_part.part_number + ' BOM'
