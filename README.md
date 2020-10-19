# Project description
A Django based eCommerce Website using multiple techs like Bootstrap, AJAX, JavaScript to improve frontend experience. Integrated third party API - Stripe to leverage payment service. Deployed on Heroku and used AWS to store and retrieve files.

Users are able to register, manage accounts and orders, post feedbacks, check purchased / viewed products history and do shopping.

# Functions
- Accounts:
   - Registration
   - Login
   - Password reset
   - Password change
   - Email activation
   - Update details (Name only currently)
   - Confirgurations (Email Marketing Prefernce)
   - Payment method
   - Address
   - Viewd history
   - Purchased history
   - Orders check

- Products:
   - Featured products will be seen at home page
   - Purchase
   - View
   - Add to a cart or remove from a cart (JavaScript)
   - Library (for digital products to download files)

- Orders:
   - Different order status (created, paid, shipped, refunded)

- Carts:
   - Checkout by cards
   - Update the and showd how many items in the cart on navbar(JavaScript)

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

# To use:
- 1. Run git clone https://github.com/austin89213/Ecommerce_Website in terminal / cmd to clone or download the file directly
- 2. Create an virtual env with Python 3 and Pip
- 3. Run terminal / cmd and cd to the main directory
- 4. Run 'pip install -r requirements.txt'
- 4. Run 'python manage.py createsuperuser' for the logging in
- 5. Run 'python manage.py runserver'
- 6. Open the url provided (http://127.0.0.1:8000/)
