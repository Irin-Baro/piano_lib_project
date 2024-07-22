from django.contrib import admin

from songs.models import SongFile
from .models import Cart, CartItem, Product


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1
    readonly_fields = ('get_total_price',)
    can_delete = True  # Добавляем возможность удаления элементов корзины


class SongFileInline(admin.TabularInline):
    model = SongFile
    extra = 1
    fields = ('song', 'file', 'difficulty')
    readonly_fields = ('difficulty',)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_price')
    search_fields = ('user__username',)
    empty_value_display = '-пусто-'
    # prepopulated_fields = {'slug': ('name',)}
    inlines = [CartItemInline]
    ordering = ('user__username',)


@admin.register(Product)
class ProductFileAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'song_file',
                    'price',)
    search_fields = ('name', 'song_file__song__song_title')
    empty_value_display = '-пусто-'
    ordering = ('song_file__song__song_title',)


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'get_total_price')
    list_filter = ('cart__user', 'product')
    search_fields = ('cart__user__username', 'product__title')
    ordering = ('cart__user__username',)

    def get_total_price(self, obj):
        return obj.get_total_price()
    get_total_price.short_description = 'Общая цена'

    def product_title(self, obj):
        return obj.song_file.song.song_title if obj.song_file else '-пусто-'
    product_title.short_description = 'Название продукта'
