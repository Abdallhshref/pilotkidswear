from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    coupon_code = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Coupon Code (Optional)'})
    )

    class Meta:
        model = Order
        fields = ['full_name', 'email', 'phone_number', 'address', 'city']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Email Address'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Phone Number'}),
            'address': forms.Textarea(attrs={'class': 'form-input', 'placeholder': 'Shipping Address', 'rows': 3}),
            'city': forms.Select(attrs={'class': 'form-input'}),
        }

from django.utils.translation import gettext_lazy as _

class OrderTrackingForm(forms.Form):
    tracking_id = forms.UUIDField(label=_("Tracking ID"), widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': _('Enter your Order ID')}))
