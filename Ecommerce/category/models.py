from django.db import models
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=128, unique=True, allow_unicode=True)
    description = models.TextField(max_length=256, blank=True)
    cat_image = models.ImageField(upload_to='photos/categories', blank=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories' # Определяет имя во множественном числе в форме(admin)
        # (по умолчанию добавляется 's')
    def get_url(self):
        return reverse('store:products-by-category', args=[self.slug])
    """
    Дает url на store_view из app store"""

    def __str__(self):
        return self.category_name