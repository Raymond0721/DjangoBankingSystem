import re
from django import forms
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import Bank, Branch


class BankForm(forms.Form):
    name = forms.CharField(max_length=120,
                           widget=forms.TextInput(attrs={'placeholder': 'Bank Name'}), required=False)
    description = forms.CharField(max_length=120,
                                  widget=forms.TextInput(attrs={'placeholder': 'Description'}), required=False)
    inst_num = forms.CharField(max_length=120,
                               widget=forms.TextInput(attrs={'placeholder': 'Institution Number'}), required=False)
    swift_code = forms.CharField(max_length=120,
                                 widget=forms.TextInput(attrs={'placeholder': 'Swift Code'}), required=False)

    def clean(self):
        super().clean()  # Don't forget to call the parent's clean method
        required_fields = ['name', 'description', 'inst_num', 'swift_code']
        if not all(self.cleaned_data.get(field) for field in required_fields):
            raise ValidationError("All fields are required.")
        return self.cleaned_data

    def save(self, curr_user):
        if not self.is_valid() or not curr_user.is_authenticated:
            return None
        data = self.cleaned_data
        return Bank.objects.create(
            name=data['name'],
            description=data['description'],
            inst_num=data['inst_num'],
            swift_code=data['swift_code'],
            owner=curr_user
        )


class BranchForm(forms.Form):
    name = forms.CharField(max_length=120,
                           widget=forms.TextInput(attrs={'placeholder': 'Branch Name'}),
                           required=False)
    transit_num = forms.CharField(max_length=120,
                                  widget=forms.TextInput(attrs={'placeholder': 'Transit Number'}),
                                  required=False)
    address = forms.CharField(max_length=120,
                              widget=forms.TextInput(attrs={'placeholder': 'Address'}),
                              required=False)
    email = forms.CharField(max_length=120,
                            widget=forms.TextInput(attrs={'placeholder': 'Email'}),
                            required=False)
    capacity = forms.CharField(widget=forms.NumberInput(attrs={'placeholder': 100}),
                               required=False)
    last_modified = forms.DateTimeField(required=False)

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name == "":
            raise forms.ValidationError("This field is required")
        return name

    def clean_transit_num(self):
        transit_num = self.cleaned_data.get('transit_num')
        if transit_num == "":
            raise forms.ValidationError("This field is required")
        return transit_num

    def clean_address(self):
        address = self.cleaned_data.get('address')
        if address == "":
            raise forms.ValidationError("This field is required")
        return address

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email == "":
            self.add_error('email', "This field is required")
            self.add_error('email', "Enter a valid email address")
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            self.add_error('email', "Enter a valid email address")
        return email

    def clean_capacity(self):
        capacity = self.cleaned_data.get('capacity')
        if not capacity:
            return None
        else:
            try:
                capacity = int(capacity)
            except ValueError:
                raise forms.ValidationError("Enter a valid number.")
            if capacity < 0:
                raise forms.ValidationError("Enter a positive number.")

        return capacity

    def save(self, curr_user, bank):
        if not self.is_valid() or not curr_user.is_authenticated:
            return None
        data = self.cleaned_data
        return Branch.objects.create(
            name=data['name'],
            transit_num=data['transit_num'],
            address=data['address'],
            email=data['email'],
            capacity=data['capacity'],
            bank=bank,
            last_modified=timezone.now()
        )
