import doctest
from django.test import TestCase


# Create your tests here.
from purchase.models import ItemValue
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

    def test_item_base_wrapper(self):
        """Animals that can speak are correctly identified"""
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
