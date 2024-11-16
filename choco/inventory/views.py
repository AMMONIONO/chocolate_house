from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product, Ingredient, ProductIngredient, Order, OrderItem
from django.db import transaction

def get_products(request):
    products = Product.objects.filter(available=True)
    return render(request, 'product_list.html', {
        "products": products
    })

def get_ingredients(request):
    ingredients = Ingredient.objects.all()
    return render(request, 'ingredient_list.html', {
        "ingredients": ingredients
    })

def place_order(request):
    if request.method == 'POST':
        print(request.POST)
        data = request.POST
        product_ids = [data[x] for x in data if x[:1] == "v"]
        customer_name = data.get('customer_name', 'Guest')

        total_price = 0
        unavailable_products = []
        order = Order(customer_name=customer_name)
        order.save()
        try:
            with transaction.atomic():
                for product_id in product_ids:
                    product = Product.objects.filter(id=product_id, available=True).first()
                    if not product:
                        unavailable_products.append(product_id)
                        continue

                    total_price += product.price
                    OrderItem.objects.create(order=order, product=product)

                    print("product, ",product)
                    for ingredient in product.ingredients.all():
                        print("ingre, ", ingredient)
                        if ingredient.stock > 0:
                            ingredient.stock -= 1 
                            ingredient.save()
                        else:
                            unavailable_products.append(product_id)
                            break

        except Exception as e:
            return HttpResponse(f"An error occurred while processing the order: {e}", status=500)

        if unavailable_products:
            return HttpResponse(f"Some products are unavailable due to ingredient stock shortage. Products: {unavailable_products}", status=400)

        discount = 0.05 + (0.01 * (total_price // 100))
        final_price = total_price * (1 - discount)
        order.total_price = total_price
        order.final_price = final_price
        order.discount = discount
        order.save()

        return HttpResponse(f"Order placed successfully. Order ID: {order.id}, Total Price: {total_price}, Final Price: {final_price}, Discount: {discount * 100}%")


    return render(request, 'order_error.html', {
        'message': 'Invalid request method'
    })

def home(request):
    products = Product.objects.all()
    return render(request, 'index.html', {
        "products": products
    })

def order_history(request):
    orders = Order.objects.all().order_by('-created_at')  # Get all orders, ordered by creation time
    return render(request, 'order_history.html', {
        "orders": orders
    })


def calculate_discount(total_price):
    if total_price > 100:
        discount = 0.05 + (0.01 * (total_price // 100))
        return discount
    return 0
def refill_page(request):
    ingredients = Ingredient.objects.all()  # Get all ingredients and their stock
    products = Product.objects.all()  # Get all products for displaying their prices
    if request.method == 'POST':
        ingredient_id = request.POST.get('ingredient_id')  # Get ingredient id
        refill_amount = int(request.POST.get('refill_amount'))  # Get amount to refill
        
        try:
            # Refill the ingredient stock
            ingredient = Ingredient.objects.get(id=ingredient_id)
            ingredient.stock += refill_amount
            ingredient.save()

            # Optional: Redirect back to refill page after success
            return redirect('refill_page')

        except Ingredient.DoesNotExist:
            return HttpResponse("Ingredient not found.", status=404)

    return render(request, 'refill_page.html', {
        'ingredients': ingredients,
        'products': products
    })