from django.db import models
from billing.models import BillingProfile
# Create your models here.
ADDRESS_TYPES=(
    ('billing','Billing'),
    ('shipping','Shipping'),
)
class Address(models.Model):
    billing_profile = models.ForeignKey(BillingProfile,on_delete=models.CASCADE)
    address_type = models.CharField(max_length=120,choices=ADDRESS_TYPES)
    address_line_1 = models.CharField(max_length=120)
    address_line_2 = models.CharField(max_length=120, null=True, blank=True)
    city = models.CharField(max_length=120)
    country= models.CharField(max_length=120, default='Taiwan')
    state = models.CharField(max_length=120, null=True, blank=True)
    postal_code = models.CharField(max_length=120)

    def __str__(self):
        if self.state:
            return f'{self.address_line_1} {self.address_line_2} {self.city} {self.country} {self.state} {self.postal_code}'
        else:
            return f'{self.address_line_1} {self.address_line_2} {self.city} {self.country} {self.postal_code}'

    def get_address(self):
        return f"{self.address_line_1}\n{self.address_line_2}\n{self.city}\n{self.state}\n{self.postal_code}\n{self.country}"
