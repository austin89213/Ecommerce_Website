# Checkout Process

1.Cart → Checkout View
  - Login / Registrer or Enter an Email(as Guest)
  - Shipping Address
  - Billing info
    -Billing Address
    -Credit Cart / Payment

2.Billing App / Component
  - Billing Profile
    - User or Email(Guest Email)
    - Generate payment processor token (Stripe or Braintree)

3.Orders / Invoices Component
  - Connecting the Billing Profile
  - Shipping / Billing Address
  - Cart
  - Status -- Shipped? Canclled?


  4.Backup Fixtures
    python manage.py dumpdata products --format json --indent 4 > products/fixtures/products.json
