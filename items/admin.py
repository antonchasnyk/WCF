from django.contrib import admin

# Register your models here.
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


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    readonly_fields = ['price']
    exclude = ['_price']
    list_display = ('part_number', 'subcategory', 'value', 'value_units')
    list_filter = ('subcategory__category', 'subcategory')
    inlines = [BOMInline, UsedInInline]
