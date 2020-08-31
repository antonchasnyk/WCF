from django.contrib import admin

# Register your models here.
from purchase.models import ItemPrice


@admin.register(ItemPrice)
class ItemPriceAdmin(admin.ModelAdmin):
    model = ItemPrice
    list_display = ('item', 'price', 'created_at')
    readonly_fields = ['created_at', 'updated_at']