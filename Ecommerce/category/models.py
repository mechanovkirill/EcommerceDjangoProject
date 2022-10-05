from django.db import models

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=128, unique=True)
    description = models.TextField(max_length=256, blank=True)
    cat_image = models.ImageField(upload_to='photos/categories', blank=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories' # Определяет имя во множественном числе в форме(admin)  (по умолчанию добавляется 's')

    def __str__(self):
        return self.category_name