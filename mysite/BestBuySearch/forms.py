# -*- coding: utf-8 -*-

from django import forms

from django.contrib.auth.forms import UserCreationForm

from django.db import transaction

from .models import Vendor, User, Customer, VendorProduct
#from django.contrib.auth.models import User

class CustomerSignUpForm(UserCreationForm):
    Agree_Terms = forms.BooleanField(required=True, label="I agree to the Terms and Conditions")
    
    class Meta(UserCreationForm.Meta):
        """Signup redef'd user."""
        model = User
        
    @transaction.atomic
    def save(self, commit = True):
        """
            Atomically save user as customer.
            Can override to not commit save.
        """
        user = super().save(commit = False)
        user.is_customer = True
        if (commit):
            user.save()
        #create new customer: 
        customer = Customer.objects.create(user = user)
        return user
    
class VendorSignUpForm(UserCreationForm):
    """Add brand name field to default vendor sign up."""

    brand = forms.CharField(required = True, label="Brand Name")
    Agree_Terms = forms.BooleanField(required=True, label="I agree to the Terms and Conditions")
    
    class Meta(UserCreationForm.Meta):
        """Signup redef'd user."""
        model = User
        
    @transaction.atomic
    def save(self):
        """
            Atomically save user as vendor.
        """
        user = super().save(commit = False)
        user.is_vendor = True
        user.save()
        #make sure brand data saved by adding entry: 
        vendor = Vendor.objects.create(user = user, brand = self.cleaned_data['brand'])
        return user

class RequirementForm(forms.Form): #forms.ModelForm):
    """Form for requirements search."""
    #override cost input to be options
    ANY = 0
    LTE_50 = 50
    LTE_100 = 100
    LTE_500 = 500
    COST_CHOICES = (
        (ANY, "Any"),
        (LTE_50, "<= $50"),
        (LTE_100, "<= $100"),
        (LTE_500, "<= $500"),
    )
    cost = forms.ChoiceField(choices = COST_CHOICES)

    #add NONE field to default category search
    NONE = 0
    CATEGORY_CHOICES = (
        (NONE, "None"),
    ) + VendorProduct.CATEGORY
    category = forms.ChoiceField(choices=CATEGORY_CHOICES)

    #ordering
    PUB_DATE = 1
    RECENTLY_UPDATED = 2
    PRICE_ASC = 3
    PRICE_DESC = 4
    ORDERING_CHOICES = (
        (NONE, "None"),
        (PUB_DATE, "Published Date"),
        (RECENTLY_UPDATED, "Recently Updated"),
        (PRICE_ASC, "Price (Low to High)"),
        (PRICE_DESC, "Price (High to Low)"),
    )
    ordering = forms.ChoiceField(choices=ORDERING_CHOICES)
    
    #payment type (mapped from model choices)
    #payment_type = forms.ChoiceField(choices = VendorProduct.PAYMENT_TYPE)

    #add ANY field to default payment type search
    # specified as 0 above
    PAYMENT_CHOICES = (
        (ANY, "Any"),
    ) + VendorProduct.PAYMENT_TYPE
    payment_type = forms.ChoiceField(choices=PAYMENT_CHOICES)

    class Meta:
        model = VendorProduct
        fields = [ 'cost', 'ordering', 'category', 'payment_type']