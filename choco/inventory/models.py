from django.db import models

# Create your models here.
from django.db import models



class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    stock = models.IntegerField()
    allergy_info = models.TextField(null=True, blank=True)


    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    description = models.TextField()
    price = models.FloatField()
    available = models.BooleanField(default=True)
    ingredients = models.ManyToManyField(Ingredient, related_name='products')

    def __str__(self):
        return self.name
    
    def get_allergens(self):
        # Get all the allergens associated with the ingredients of this product
        allergens = set()
        product_ingredients = ProductIngredient.objects.filter(product=self)
        for product_ingredient in product_ingredients:
            ingredient = product_ingredient.ingredient
            if ingredient.allergy_info:
                allergens.update(ingredient.allergy_info.split(","))
        return allergens

class ProductIngredient(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField()


class Order(models.Model):
    customer_name = models.CharField(max_length=100)
    total_price = models.FloatField(null=True)
    final_price = models.FloatField(null=True)
    discount = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.customer_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
