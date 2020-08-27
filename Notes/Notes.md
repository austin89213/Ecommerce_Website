

cookies / sessions:
1. Using cookies to keep the products in the carts for users to use next time even they didn't login


JS / jQuery - static/js
1. Improving the search fucntion by JavaScript -- Make it auto search and change the button when searching
2. Using JS to add / remove items from the cart, which makes it no need to refresh the page each time we clicked on the add / remove button.
It also changed the number of items in the cart in navbar!
(However, there's a bug in cart page. So I don't use JS in cart page and it still works fine)


2020/08/05
1.Using jQuery Confirm in contact form - static/js
2.Using jQuery to modify the contact form - static/js

2020/08/06
1. Custom User Model(Using AbstractBaseUser, BaseUserManager) - accounts.admin/models
refer:https://www.codingforentrepreneurs.com/blog/how-to-create-a-custom-django-user-model/
2. Using Fixtures to handle database aftet the user model changed(Reload) -products
3. Upadteing Login/Register (FBV to CBV): - accounts.view
    Login : username → Email
    Register : use UserAdminCreationForm, but not active (then send an confirmation email)

2020/08/10
1. Custom Analytics (User Analytics)
refer:https://www.codingforentrepreneurs.com/blog/custom-analytics-with-django/#watch
2. Using Signal, GenericForeignKey, ContentType
3. Using siganl,mixin,multiple inheritance, instance.__class__
4. Modifing User Seesion (one user to one session one time,)

2020/08/11
1. Stripe API  - Billling.models,https://stripe.com/docs/api/issuing/cards
2. jsRender https://www.jsviews.com/
3. # Must retrieve the customer before adding a card, otherwise it won't connect to each other.
4. Improve the Finalize Checkout Page to select a payment method

2020/08/16
1. Mailchimp
API using:https://mailchimp.com/developer/api/marketing/list-members/update-list-member/
Course:https://www.codingforentrepreneurs.com/blog/mailchimp-integration/

2020/08/17
1.redirct("the url-1 you want to go, ?next= url-2 after you action in url-1")
*Have to set up 'next' in the view of url-1. In this caee, refer the accoutns.views.LoginView
2.Use SuccessMessageMixin to improve the user experience (put the rendering code in base.html)
3. RequestBin - For makeing a local url able to test on a live service(Mailchimp)

Make the project live-
  (1) Make a new settings folder, rename the settings.py to base.py and put it in.
  (2) Create a __init__.py (first look at thie file when starting a project), import base.py to it
  (3) modify the BASE_DIR, put original one into another os.path.dirname()
  (4) SSL/TLS https https://www.codingforentrepreneurs.com/blog/ssltls-settings-for-django
  (5) Gitignore File

Herokui
https://www.codingforentrepreneurs.com/blog/go-live-with-django-project-and-heroku


Amazone Web Services
  https://www.codingforentrepreneurs.com/blog/s3-static-media-files-for-django
  (1) change the policy json form <your bucket name> to real bucket name
  (2) rewrite the region to where you are in aws/conf.py

Error Page handling
  Use builtin pages as templates for rendering
