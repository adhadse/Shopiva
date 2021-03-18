# Shopiva : Django personalized Ecommerce website
ML Based Ecommerce site 
## Features:
- [X] Customer can create account and sign In 
- [X] A completed product catalog page
- [X] Product Details Page
    - Features a review section when customer can review and can give rating-stars
    - Based on the average rating given by customer, the average rating is shown in catalog and product_details_page.
- [X] Add to cart functionality for customers with account created
    - Cart item quantity can be changed and/or removed on the cart page.
    - If the cart item quantity is changed the price on the pages also changes, WITHOUT RELOADING, implemented using AJAX and a Backend server API.
    - If the cart item is deleted the item is removed from the page, without a refresh, the price is reflected.
- [x] Add to Wishlist
    - Wishlist Item lists if the product price is dropped or not (The product price is saved for that particular customer along with the product and then compared to current productPrice)
- [X] Order functionality
    - Non authenticated customer can't make a purchase, hence the button is disabled
    - Once an order is made, a transaction id is given and status is changed from 'In Cart' to 'Delivered'
    - All orders can then be seen in order history page and tractions in transactions page
    - The productPrice and quanity is also stored per order, as the actual productPrice may change overtime.
- [X] Navbar is updated everytime a product is added to cart or added to wish list, using AJAX.
- [X] Customer Profile page
---
## Installing required Dependencies. 

***Make sure you import project in a virtual Environment***
```
pip install -r requirements.txt
```
---
## Common snippets
To Run Server:
```
python manage.py runserver
```
To create a new app, run
```
python manage.py startapp <projectapp>
```
For other management, run
```
python manage.py
```
# Images
![login/signin](Shopiva/images/Screenshot%202020-11-17%20194111.png)


![homepage](Shopiva/images/Screenshot%202020-11-17%20194244.png)


![productdetailspage](Shopiva/images/Screenshot%202020-11-17%20194317.png)


![cartpage](Shopiva/images/Screenshot%202020-11-17%20194351.png)


![profilepage](Shopiva/images/Screenshot%202020-11-17%20194426.png)


![orderspage](Shopiva/images/Screenshot%202020-11-17%20194454.png)


![transactionspage](Shopiva/images/Screenshot%202020-11-17%20194519.png)






