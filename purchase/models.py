from django.db import models

# Create your models here.
from django.db.models import Q
from django.utils.translation import gettext_lazy as _


class ItemPrice(models.Model):
    item = models.ForeignKey('items.Item', on_delete=models.CASCADE, null=False, blank=False)
    price = models.DecimalField(verbose_name='price', default=0.0, max_digits=10, decimal_places=3,
                                null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey('auth.User', on_delete=models.PROTECT, null=False, blank=False)

    def __str__(self):
        return str(self.item) + ' ' + str(self.created_at)


value_status = [
        ('pr', _('Preliminary')),
        ('nd', _('Needs')),
        ('or', _('Ordered')),
        ('pa', _('Paid')),
        ('ow', _('On the way')),
        ('dn', _('Done')),
    ]

value_reason = [
        ('pu', _('Purchase')),
        ('mf', _('Manufacturing')),
        ('rp', _('Repair')),
        ('uc', _('User correction')),
]


class DoneValueManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(Q(status='dn') & Q(reason='pu'))


class NeedsValueManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(Q(status='nd') & Q(reason='pu'))


class InProgressValueManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(reason='pu').filter(Q(status='or') |
                                                                 Q(status='pa') |
                                                                 Q(status='ow'))


class ItemValue(models.Model):
    item = models.ForeignKey('items.Item', on_delete=models.PROTECT, null=False, blank=False, related_name='item_value')
    value = models.IntegerField(default=0, verbose_name=_('Value'), null=False, blank=False)
    status = models.CharField(max_length=2, verbose_name=_('Status'), choices=value_status,
                              default='nd', null=False, blank=False)
    reason = models.CharField(max_length=2, verbose_name=_('Reason'), choices=value_reason,
                              default='pu', null=False, blank=False)
    assembly_part = models.ForeignKey('items.Item', on_delete=models.PROTECT,
                                      null=True, blank=True, related_name='value_used_in')
    price = models.DecimalField(verbose_name='price', default=0.0, max_digits=10, decimal_places=3,
                                null=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey('auth.User', on_delete=models.PROTECT, null=False, blank=False)

    objects = models.Manager()
    objects_done = DoneValueManager()
    objects_in_progress = InProgressValueManager()
    objects_needs = NeedsValueManager()

    class Meta:
        permissions = (
            ("can_order", _("Can order needs")),
            ("can_pay", _("Can pay ordered")),
            ("can_deliver", _("Can make delivery")),
            ("can_done", _("Can accept to warehouse")),
        )

    def __str__(self):
        return '{} value:{} status:{}'.format(str(self.item.designator()), str(self.value), str(self.status))


class Proforma(models.Model):
    pass
