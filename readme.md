How to Run the Application
Prerequisites
Python 3.x
Django 3.x or higher
Docker (for containerization)
1. Clone the Repository
bash
Copy code
git clone <repository_url>
cd chocolate-house
2. Set Up the Virtual Environment
Create a virtual environment:

bash
Copy code
python -m venv venv
Activate the virtual environment:

For Windows:

venv\Scripts\activate

3. Install Dependencies
Install the required Python packages from requirements.txt:

bash
Copy code
pip install -r requirements.txt
4. Run Database Migrations
Set up the database schema by running Django's migrations:

bash
Copy code
python manage.py migrate
5. Create a Superuser
Create a superuser to access the Django admin panel:

bash
Copy code
python manage.py createsuperuser
Follow the prompts to set up the username, email, and password.

6. Run the Development Server
Start the Django development server:

bash
Copy code
python manage.py runserver
Visit the application in your web browser at http://127.0.0.1:8000/.

Testing the Application
1. Manual Testing
Testing Product Ordering and Stock Reduction
Navigate to the Product Page: Visit the product page to view all available products. Check if products are listed correctly with their allergen information and availability.

Place an Order:

Select products to add to your order.
Fill in the customer name.
Submit the order form.
Check Ingredient Stock:

After placing the order, verify that the stock of ingredients used in the ordered products is reduced accordingly.
For example, if a Chocolate Truffle Cake requires Butter and Sugar, check that the stock of these ingredients is decreased by the quantities required for that product.
Check for Allergen Information:

Ensure that products with allergens display the correct allergen information on the product page.
Validate Discount Logic:

Check if the discount is applied correctly based on the total price of the order.
Testing Admin Features
Log in to Admin Panel:
Navigate to http://127.0.0.1:8000/admin/ and log in using the superuser credentials.
Add New Product:
In the admin panel, add a new product with associated ingredients and allergen information.
Refill Ingredient Stock:
Add or refill stock for ingredients used in products.
Check Order Management:
Check the orders placed by customers in the admin panel. Ensure that the stock levels update correctly when an order is placed.
2. Automated Tests (Optional)
You can also run Django's built-in test suite to validate the functionality of your models, views, and forms.

bash
Copy code
python manage.py test
This will run all the tests defined in the tests.py file.

SQL Queries for Product, Ingredient, and Order Management
Below are some SQL queries to help with testing and managing data directly in the database:

1. Add Products and Ingredients
sql
Copy code
-- Add Products
INSERT INTO product (name, category, description, price, available) 
VALUES ('Date Walnut Cake', 'Cake', 'A delicious walnut cake with dates', 10.00, true),
       ('Chocolate Truffle Cake', 'Cake', 'Rich chocolate truffle cake', 12.00, true);

-- Add Ingredients
INSERT INTO ingredient (name, stock, allergy_info) 
VALUES ('Dark Chocolate', 100, 'Contains dairy'),
       ('Butter', 150, 'Contains milk'),
       ('Sugar', 200, 'No allergens'),
       ('Eggs', 50, 'Contains eggs'),
       ('Flour', 300, 'No allergens');
2. Link Ingredients to Products
sql
Copy code
-- Link Ingredients to Products
INSERT INTO product_ingredient (product_id, ingredient_id, quantity)
VALUES (1, 1, 20), -- Date Walnut Cake uses 20 units of Dark Chocolate
       (1, 2, 10), -- Date Walnut Cake uses 10 units of Butter
       (2, 1, 30), -- Chocolate Truffle Cake uses 30 units of Dark Chocolate
       (2, 3, 15); -- Chocolate Truffle Cake uses 15 units of Sugar
3. Add an Order
sql
Copy code
-- Add Order
INSERT INTO order (customer_name, total_price, final_price, discount, created_at) 
VALUES ('John Doe', 24.00, 22.80, 5, '2024-11-16 12:00:00');

-- Add Order Items
INSERT INTO order_item (order_id, product_id)
VALUES (1, 1),  -- Date Walnut Cake
       (1, 2);  -- Chocolate Truffle Cake
4. Reduce Ingredient Stock
sql
Copy code
-- After an order is placed, reduce ingredient stock based on the products ordered
UPDATE ingredient SET stock = stock - 20 WHERE id = 1;  -- Dark Chocolate
UPDATE ingredient SET stock = stock - 10 WHERE id = 2;  -- Butter
UPDATE ingredient SET stock = stock - 30 WHERE id = 3;  -- Sugar


docker-compose up --build
This will start the Django development server inside a Docker container. You can visit the application at http://127.0.0.1:8000/.