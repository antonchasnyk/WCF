import os

from django.db import models
from django.db.models import Sum, Q, UniqueConstraint
from django.dispatch import receiver
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext_lazy as _
import re

from WCF import settings

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

    >>> unit_conversion('pcs', 'kpcs', 10)
    (10, 'pcs')

    >>> unit_conversion('kpcs', 'pcs', 10)
    (10, 'kpcs')

    >>> unit_conversion('pF', 'pF', 10)
    (10, 'pF')

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
        'p': 1E-12,
        'n': 1E-9,
        'u': 1E-6,
        'm': 1E-3,
        '': 1,
        'k': 1E3,
        'M': 1E6,
        'G': 1E9,
    }

    if 'pcs' in source or 'pcs' in target:
        return value, source
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
        return super().get_queryset()\
            .annotate(value=Sum('item_value__value', filter=Q(item_value__status='dn')))\
            .prefetch_related('subcategory').order_by('subcategory__name', 'part_number')


class ComponentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().annotate(value=Sum('item_value__value',
                                                         filter=Q(item_value__status='dn')))\
            .filter(item_type='co').prefetch_related('subcategory').order_by('subcategory__name', 'part_number')


class AssemblyPartsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().annotate(value=Sum('item_value__value',
                                                         filter=Q(item_value__status='dn')))\
            .filter(item_type='ap').prefetch_related('subcategory').order_by('subcategory__name', 'part_number')


class ConsumableManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().annotate(value=Sum('item_value__value',
                                                         filter=Q(item_value__status='dn')))\
            .filter(item_type='cm').prefetch_related('subcategory').order_by('subcategory__name', 'part_number')


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
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    objects = models.Manager()
    valued_objects = ValuedManager()
    components = ComponentManager()
    assembly_parts = AssemblyPartsManager()
    consumable = ConsumableManager()

    class Meta:
        ordering = 'part_number', 'subcategory__name'
        indexes = [
            models.Index(fields=['part_number']),
            models.Index(fields=['comment']),
            models.Index(fields=['subcategory']),
            models.Index(fields=['item_type']),
        ]

    def __str__(self):
        return self.part_number

    def get_value(self):
        value = self.item_value.aggregate(value=Sum('value', filter=Q(status='dn')))['value']
        return value if value else 0

    def get_value_set(self):
        return self.item_value.filter(status='dn').order_by("-updated_at")

    def designator(self):
        return self.comment + ' ' + self.part_number if self.comment else self.part_number

    def get_absolute_url(self):
        if self.item_type == 'co':
            return reverse_lazy('items:detail_component', kwargs={'component_id': self.pk})
        elif self.item_type == 'ap':
            return reverse_lazy('items:detail_assembly', kwargs={'assembly_id': self.pk})
        elif self.item_type == 'cm':
            return reverse_lazy('items:detail_consumable', kwargs={'component_id': self.pk})

    def get_edit_url(self):
        if self.item_type == 'co':
            return reverse_lazy('items:edit_component', kwargs={'component_id': self.pk})
        elif self.item_type == 'ap':
            return reverse_lazy('items:edit_assembly', kwargs={'component_id': self.pk})
        elif self.item_type == 'cm':
            return reverse_lazy('items:edit_consumable', kwargs={'component_id': self.pk})


class ItemCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Category name'), unique=True, null=False, blank=False)

    class Meta:
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name


class ItemSubCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Sub Category name'), unique=False,
                            null=False, blank=False)
    category = models.ForeignKey('ItemCategory', verbose_name=_('Category'), on_delete=models.PROTECT,
                                 null=False, blank=False)
    parent = models.ForeignKey(to='self', null=True, blank=True, related_name='child_subcategory',
                               on_delete=models.PROTECT)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['name', 'parent'], name='items_unique_subcategory')
        ]
        ordering = ['name', 'category__name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['parent']),
        ]

    def __str__(self):
        if self.parent:
            return self.name + ' ' + str(self.parent)
        else:
            return self.name + ' ' + self.category.name

    def get_path(self, path=None):
        if path is None:
            path = []
        if self.parent:
            path.append(self)
            self.parent.get_path(path)
        else:
            path.append(self)
        return path

    @classmethod
    def get_roots(cls):
        return cls.objects.filter(parent=None)

    def get_children(self):
        return self.__class__.objects.filter(parent=self)


class DocType(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Document type'), unique=True, null=False, blank=False)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name


def get_doc_file_path(instance, filename):
    path = os.path.join('items_docs/{}/{}s/'.format(instance.item.part_number,
                                                    instance.doc_type.name),
                        '{}_{}{}'.format(instance.item.part_number,
                                         instance.doc_type,
                                         os.path.splitext(instance.document.name)[1]))
    return path


class ItemDocFile(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='document')
    doc_type = models.ForeignKey(DocType, verbose_name=_('Document type'), on_delete=models.PROTECT,
                                 related_name='document')
    document = models.FileField(upload_to=get_doc_file_path,  null=False, verbose_name=_("Document"), max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False,)

    def filename(self):
        return os.path.basename(self.document.name)


@receiver(models.signals.post_delete, sender=ItemDocFile)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.document:
        if os.path.isfile(instance.document.path):
            os.remove(instance.document.path)


@receiver(models.signals.pre_save, sender=ItemDocFile)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_file = sender.objects.get(pk=instance.pk).document
    except sender.DoesNotExist:
        return False

    new_file = instance.document
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)


class BOM(models.Model):
    item = models.ForeignKey('Item', on_delete=models.PROTECT, related_name='used_in')
    assembly_part = models.ForeignKey('Item', on_delete=models.CASCADE, related_name='consist_of')
    position = models.CharField(max_length=200, verbose_name=_('RefDes'),
                                unique=False, null=False, blank=False)
    quantity = models.IntegerField(default=0, verbose_name=_('Quantity'), null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        indexes = [
            models.Index(fields=['item']),
            models.Index(fields=['assembly_part']),
            models.Index(fields=['item', 'assembly_part']),
        ]

    def __str__(self):
        return self.assembly_part.part_number + ' BOM'
