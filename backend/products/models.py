import random
from django.urls import reverse
from django.conf import settings
from django.db import models
from django.db.models import Q
User = settings.AUTH_USER_MODEL

TAGS_MODEL_VALUES = ['electronics', 'cars', 'boats', 'movies', 'cameras' ]



#  Manually creating a queryset to search
class ProductQuerySet(models.QuerySet):
    def is_public(self):
        return self.filter(public=True)
      
    # check insidde the title and content if the query exists in it. 
    def search(self, query, user=None):
        lookup = Q(title__icontains=query) | Q(content__icontains=query) # Q allows us to write our lookups the way i did there
        qs = self.is_public().filter(lookup)
        # if user is not none show the user all his data public o rnot
        if user is not None:
            qs2 = qs.filter(user=user)
            qs = (qs | qs2).distinct()
        return qs
        
# Object manager to easily get a filter result from the db
class ProductManaager(models.Manager):

    def get_queryset(self, *args, **kwargs):
        return ProductQuerySet(self.model, using=self.db)

    def search(self, query, user=None):
        return self.get_queryset().search(query, user=user)


class Product(models.Model):
    user = models.ForeignKey(User, null=True ,on_delete=models.SET_NULL, default=1,)
    title = models.CharField(max_length=200)
    content = models.CharField(max_length=200, blank=True, null=True)
    price = models.DecimalField(max_digits=15, decimal_places=2, default=9.99)
    public = models.BooleanField(default=True)
    objects = ProductManaager()
    
    def is_public(self):
        return self.public
    
    
    def get_absolute_url(self):
        return reverse("products:product-detail", kwargs={'pk':self.pk})
        # return f"/api/products/{self.pk}/"
    
    
    @property
    def body(self):
        return self.content
    
    @property
    def endpoint(self):
        return self.get_absolute_url()
    
    @property
    def path(self):
        return f"/product/{self.pk}/"
    
    @property
    def sale_price(self):
        return "%.2f" % (float(self.price) * 0.8)

    def get_discount(self): return round(float(self.sale_price) * 0.01, 2)
    
    def get_tags_list(self):
        return [random.choice(TAGS_MODEL_VALUES)]
