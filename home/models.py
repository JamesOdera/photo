from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from datetime import datetime
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
import math
from cloudinary.models import CloudinaryField

class Category(models.Model):
    name = models.CharField(max_length=30, blank=False, null=False)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

class Image(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=120)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = CloudinaryField('blog-image')
    description = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    featured = models.BooleanField(default=False, null=True, blank=True)
    
    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('image_detail', args=[self.id, self.slug])
    
    
@receiver(pre_save, sender=Image)
def pre_save_slug(sender, **kwargs):
    slug = slugify(kwargs['instance'].title)
    kwargs['instance'].slug = slug
    
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    photo = CloudinaryField('blog-image-profile')
    # photo = models.ImageField(upload_to='profile_pictures', blank=True, null=True)
    

    def __str__(self):
        return "Profile of User {}".format(self.user.username)
