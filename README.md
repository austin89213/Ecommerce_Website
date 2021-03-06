# Project description
A Django based eCommerce Website using Bootstrap, jQuery to improve frontend experience. Integrated third party API - Stripe to leverage payment service. Deployed on Heroku and used AWS to store and retrieve files.

Users are able to register, manage accounts and orders, post feedbacks, check purchased / viewed products history and do shopping.

# Functions
- Accounts:
   - Registration
   - Login
   - Password reset
   - Password change
   - Email activation
   - Update details (Name only currently)
   - Payment method
   - Address
   - Viewd history
   - Purchased history
   - Orders check

- Products:
   - Featured products will be seen at home page
   - Purchase
   - View (Viewed times would be recorded)
   - Add to a cart or remove from a cart (jQuery)
   - Digital Attribute
   - Library (for digital products to download files)

- Orders:
   - Different order status (created, paid, shipped, refunded)

- Carts:
   - Checkout by cards
   - Update the cart and show how many items in it on navbar (jQuery)

- Charges:
   - Integrate Stripe API as the payment platform

- Contacts:
   - Provide a contact form to collect advices

- Navabar:
   - Link of the current path will be lighter to notice which page the users are

- Others:
   - RWD

# Techniques & tools :

- Backend:
   - Django (3.0.3) (https://www.djangoproject.com/)

- Frontend:
   - Bootstrap (4) (https://getbootstrap.com/)
   - jQuery(3.5) (https://jquery.com/)

- Database:
   - SQLite (https://www.sqlite.org/index.html)

- Deployment:

   - AWS (https://aws.amazon.com/)
   - Heroku (https://www.heroku.com/)

- Third Part API:
   - Stripe (https://stripe.com/)
