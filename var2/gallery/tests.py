from django.test import TestCase
from django.urls import reverse
from .models import Category, Image
from django.core.files.uploadedfile import SimpleUploadedFile
import datetime

class GalleryViewTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Nature')
        image_file = SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
        self.image = Image.objects.create(
            title='Test Image',
            image=image_file,
            created_date=datetime.date.today(),
            age_limit=18
        )
        self.image.categories.add(self.category)

    def test_gallery_view_status_code(self):
        url = reverse('gallery_view')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_gallery_view_template_used(self):
        url = reverse('gallery_view')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'gallery.html')

    def test_gallery_view_context(self):
        url = reverse('gallery_view')
        response = self.client.get(url)
        self.assertIn('categories', response.context)
        self.assertIn(self.category, response.context['categories'])


class ImageDetailViewTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Nature')
        image_file = SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
        self.image = Image.objects.create(
            title='Test Image',
            image=image_file,
            created_date=datetime.date.today(),
            age_limit=18
        )
        self.image.categories.add(self.category)

    def test_image_detail_view_status_code(self):
        url = reverse('image_detail', kwargs={'pk': self.image.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_image_detail_template_used(self):
        url = reverse('image_detail', kwargs={'pk': self.image.pk})
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'image_detail.html')

    def test_image_detail_context(self):
        url = reverse('image_detail', kwargs={'pk': self.image.pk})
        response = self.client.get(url)
        self.assertIn('image', response.context)
        self.assertEqual(response.context['image'], self.image)
