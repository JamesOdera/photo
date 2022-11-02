from django.contrib import admin

from .models import *
    
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    
class ImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'image', 'description', 'author', 'featured', 'pub_date',)
    list_filter = ('pub_date',)
    search_fields = ('author__username',)
    date_hierarchy = ('pub_date')
    
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'birth_date', 'location', 'photo', 'bio')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Profile, ProfileAdmin)