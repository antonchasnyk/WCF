import doctest
from django.test import TestCase


# Create your tests here.
from purchase.models import ItemValue, ItemPrice
from . import models
from .models import Item, ItemCategory, ItemSubCategory
from django.contrib.auth.models import User

print(doctest.testmod(models))


class ItemTestCase(TestCase):
    def setUp(self):
        cat = ItemCategory.objects.create(name='Category')
        sub1 = ItemSubCategory.objects.create(name='SubCategory1', category=cat)
        sub2 = ItemSubCategory.objects.create(name='SubCategory2', parent=sub1, category=cat)
        user = User.objects.create(username='Testuser')
        item = Item.objects.create(part_number='purtnumber_787999', comment='comment_584564',
                                   subcategory=sub2,
                                   created_by=user)
        self.price = ItemPrice.objects.create(item=item, price=10.00, created_by=user)
        self.value_pr = ItemValue.objects.create(item=item, value=1, status='pr', created_by=user, reason='pu')
        self.value_nd = ItemValue.objects.create(item=item, value=2, status='nd', created_by=user, reason='pu')
        self.value_or = ItemValue.objects.create(item=item, value=3, status='or', created_by=user, reason='pu')
        self.value_pa = ItemValue.objects.create(item=item, value=4, status='pa', created_by=user, reason='pu')
        self.value_ow = ItemValue.objects.create(item=item, value=5, status='ow', created_by=user, reason='pu')
        self.value_dn = ItemValue.objects.create(item=item, value=6, status='dn', created_by=user, reason='pu')
        self.value_mf = ItemValue.objects.create(item=item, value=7, status='dn', created_by=user, reason='mf')
        self.value_rp = ItemValue.objects.create(item=item, value=8, status='dn', created_by=user, reason='rp')
        self.value_uc = ItemValue.objects.create(item=item, value=9, status='dn', created_by=user, reason='uc')

    def test_item_base_wrapper(self):
        item = Item.objects.get(part_number="purtnumber_787999")
        cat = ItemCategory.objects.get(name="Category")
        sub1 = ItemSubCategory.objects.get(name='SubCategory1')
        sub2 = ItemSubCategory.objects.get(name='SubCategory2')
        self.assertEqual(str(item), 'purtnumber_787999')
        self.assertEqual(item.designator(), 'comment_584564 purtnumber_787999')
        self.assertEqual(str(cat), 'Category')
        self.assertEqual(str(sub1), 'SubCategory1 Category')
        self.assertEqual(str(sub2), 'SubCategory2 SubCategory1 Category')
        self.assertEqual(list(ItemSubCategory.get_roots()), [sub1])
        self.assertEqual(list(sub1.get_children()), [sub2])
        self.assertEqual(sub2.get_path(), [sub2, sub1])

    def test_itemvalue_base_wrapper(self):
        value_dn = ItemValue.objects.get(pk=self.value_dn.pk)
        done = set(ItemValue.objects.filter(status='dn'))
        self.assertEqual(done, {self.value_dn, self.value_mf, self.value_rp, self.value_uc})
        self.assertEqual(str(value_dn), '{} value:{} status:{}'.format(str(value_dn.item.designator()),
                                                                       str(value_dn.value),
                                                                       str(value_dn.status)))
        self.assertEqual(set(ItemValue.objects_done.all()), {value_dn})
        self.assertEqual(set(ItemValue.objects_needs.all()), {self.value_nd})
        self.assertEqual(set(ItemValue.objects_in_progress.all()), {self.value_or, self.value_pa, self.value_ow})

    def test_itemprice_base_wrapper(self):
        price = ItemPrice.objects.all()[0]
        item = Item.objects.get(part_number="purtnumber_787999")
        self.assertEqual(str(price), str(item) + ' {}$ '.format(price.price) + str(price.created_at) )