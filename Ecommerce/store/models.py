from django.db import models
from category.models import Category
from django.shortcuts import reverse


# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=256, unique=True)
    slug = models.SlugField(max_length=256, unique=True)
    description = models.TextField(max_length=512, blank=True)
    price = models.IntegerField()
    images = models.ImageField(upload_to='photos/products') #TODO: добавлять несколько изображений
    stock = models.IntegerField() #TODO: Автоматизация
    is_available = models.BooleanField(default=True) #TODO: Автоматизация
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('store:product-detail', args=[self.category.slug, self.slug])
    """
    Дает url на store_view из app store"""


    def __str__(self):
        return self.product_name

