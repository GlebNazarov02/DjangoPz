from django.contrib import admin
from .import models



class ProductAdmin(admin.ModelAdmin):
    @admin.action(description="Обнулить кол-во товара в наличии")
    def reset_count(modeladmin, request, queryset):
        queryset.update(count=0)

    list_display = ['name', 'price', 'amount']
    search_fields = ['name']
    search_help_text = 'Поиск по полю Описание продукта (description)'
    list_filter = ['address','email']

    readonly_fields = ['added_at']
    fieldsets = [
        (
            None, { 
                'classes': ['wide'],  
                'fields': ['name'],  
            },
        ),
        (
            'Подробности',  
            {
                'classes': ['collapse'],  
                'description': 'Товар и его подробное описание', 
                'fields': ['pname', 'description'],  
            },
        ),
        (
            'Price list',
            {
                'fields': ['cost', 'quantity'],
            }
        ),
    ]


@admin.register(models.Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'email','address']
    ordering = ['name']
    search_fields = ['name']
    search_help_text = 'Поиск по имени (name)'

    fieldsets = [
        (
            None,
            {
                'classes': ['wide'],
                'fields': ['name'],
            },
        ),
        (
            'Подробности',
            {
                'classes': ['collapse'],
                'description': 'Данные о покупателе',
                'fields': ['name', 'email' ]
            },
        ),

        (
            'Адрес',
            {
                'description': 'Адрес',
                'fields': ['address'],
            }
        ),
    ]
