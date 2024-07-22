from django.db import models
from django.contrib.auth import get_user_model

from songs.models import SongFile

User = get_user_model()


class Product(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название продукта',
        help_text='Укажите название продукта'
    )
    song_file = models.ForeignKey(
        SongFile,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Файл песни',
        help_text='Укажите файл песни, связанный с продуктом',
        blank=True,  # возможно пустое значение, если продукт - не файл
        null=True
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        if self.song_file:
            return (f'{self.name} {self.song_file.song.song_title} '
                    f'({self.song_file.difficulty})')
        return self.name


class Cart(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00
    )

    class Meta:
        verbose_name = 'Корзина пользователя'
        verbose_name_plural = 'Корзины пользователей'

    def __str__(self):
        return f'В корзине {self.user.username}'

    def update_total_price(self):
        self.total_price = sum(item.get_total_price()
                               for item in self.items.all())
        self.save()


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(
        default=1
    )

    class Meta:
        verbose_name = 'Продукт в корзине'
        verbose_name_plural = 'Продукты в корзинах'

    def __str__(self):
        return f'{self.product.name} в корзине {self.cart.user.username}'

    def get_total_price(self):
        return self.product.price * self.quantity

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.cart.update_total_price()
