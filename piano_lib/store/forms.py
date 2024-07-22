from django import forms


class PaymentForm(forms.Form):
    email = forms.EmailField(required=True)
    card_number = forms.CharField(max_length=16, required=True)
    card_expiry = forms.CharField(max_length=5, required=True)
    card_cvc = forms.CharField(max_length=3, required=True)
