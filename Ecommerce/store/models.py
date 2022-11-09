from django.db import models
from category.models import Category
from django.shortcuts import reverse
from accounts.models import Account
from django.db.models import Avg, Count
from django.core.validators import MaxLengthValidator


# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=256, unique=True)
    slug = models.SlugField(max_length=256, unique=True, allow_unicode=True)
    description = models.TextField(max_length=512, blank=True, validators=[MaxLengthValidator(512, message='Maximum value exceeded')])
    price = models.IntegerField()
    images = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    popularity = models.IntegerField(default=0)
    # article
    # size
    # color

    def get_url(self):
        """Дает url на store_view из app store"""
        return reverse('store:product-detail', args=[self.category.slug, self.slug])


    def __str__(self):
        return self.product_name

    def average_rating(self):
        """Returns the average rating value"""
        # Avg - одна из списка ['Aggregate', 'Avg', 'Count', 'Max', 'Min', 'StdDev', 'Sum', 'Variance',]
        # функций работающих с полями баз данных.
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg

    def count_reviews(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count

class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category='color', is_active=True)

    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size', is_active=True)


variation_category_choice = (
    ('color', 'color'),
    ('size', 'size')
)


class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=128, choices=variation_category_choice)
    variation_value = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)

    objects = VariationManager()

    def __str__(self):
        return self.variation_value


class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=128, blank=True,)
    review = models.TextField(max_length=512, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=24, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject


class ProductGallery(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='store/products', max_length=264)

    def __str__(self):
        return self.product.product_name

    class Meta:
        verbose_name = 'productgallery'
        verbose_name_plural = 'product gallery'