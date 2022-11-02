from django.test import TestCase
from category.models import Category
from django.core.files.uploadedfile import SimpleUploadedFile

max_length_test_params = {'category_name': 50, 'slug': 128, 'description': 256}
allow_unicode_test_params = {'slug': True}
blank_test_params = {'description': True, 'cat_image': True}
image = SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')


class CategoryTests(TestCase):
    """Тесты для модели Category"""

    @classmethod
    def setUpTestData(cls):
        """Заносит данные в БД перед запуском тестов класса"""
        cls.category = Category.objects.create(
            category_name='Category',
            slug='category',
            description='Demo description',
            cat_image='image'
        )

    def test_max_length(self):
        for key in max_length_test_params:
            instance = Category.objects.get(id=1)
            max_length = instance._meta.get_field(key).max_length
            self.assertEquals(max_length, max_length_test_params[key])

    def test_allow_unicode(self):
        for key in allow_unicode_test_params:
            instance = Category.objects.get(id=1)
            allow_unicode = instance._meta.get_field(key).allow_unicode
            self.assertEquals(allow_unicode, allow_unicode_test_params[key])

    def test_blank(self):
        for key in blank_test_params:
            instance = Category.objects.get(id=1)
            blank = instance._meta.get_field(key).blank
            self.assertEquals(blank, blank_test_params[key])

    def test_cat_image(self):
        instance = Category.objects.get(id=1)
        upload_to = instance._meta.get_field('cat_image').upload_to
        self.assertEquals(upload_to, 'photos/categories')

    def test_str_method(self):
        self.assertEquals(str(self.category), self.category.category_name)

    def test_model_verbose_name(self):
        self.assertEqual(self.category._meta.verbose_name, 'category')

    def test_model_verbose_name_plural(self):
        self.assertEqual(self.category._meta.verbose_name_plural, 'categories')

    def test_get_url(self):
        self.assertEqual(self.category.get_url(), '/store/category/category/')
