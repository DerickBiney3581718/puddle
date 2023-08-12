from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ["name"]
        
    def __str__(self):
        return self.name
    
    
    
class Item(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField(default=False)
    is_sold = models.BooleanField(default= False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name ='items', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='item_images', blank=True, null=True)
    
    def __str__(self):
        return self.name
    