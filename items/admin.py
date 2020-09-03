from django.contrib import admin

# Register your models here.
from purchase.models import ItemPrice, ItemValue
from .models import Item, ItemCategory, ItemSubCategory, BOM

admin.site.register(ItemCategory)
admin.site.register(ItemSubCategory)


class BOMInline(admin.TabularInline):
    model = BOM
    extra = 3
    fk_name = "assembly_part"


class UsedInInline(admin.TabularInline):
    model = BOM
    extra = 3
    fk_name = "item"


class PriceInInline(admin.TabularInline):
    model = ItemPrice
    extra = 3


class ValueInInline(admin.TabularInline):
    model = ItemValue
    extra = 3


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('part_number', 'subcategory', 'value_units', 'pk')
    list_filter = ('subcategory__category', 'subcategory')
    inlines = [BOMInline, UsedInInline, PriceInInline, ValueInInline]



