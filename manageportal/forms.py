from django import forms

from .models import Message


# class ContactForm(forms.ModelForm):
#     class Meta:
#         model = Contact
#         fields = [
#             'fullname',
#             'phone',
#             'email',
#             'address',
#             'description'
#         ]


class ContactForm(forms.Form):
    fullname = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter your full name',
                'class': 'form-control'
            }
        )
    )

    product_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter your product name',
                'class': 'form-control'
            }
        )
    )

    phone_number = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'placeholder': 'Enter your phone number',
                'class': 'form-control'
            }
        )
    )
    email = forms.EmailField(
        max_length=200,
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Enter your E-mail',
                'class': 'form-control'
            }
        )
    )
    address = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter your Home Address',
                'class': 'form-control'
            }
        )
    )
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Enter Product description',
                'class': 'form-control',
                'rows': 7,
                'cols': 25
            }
        ),
        max_length=2000
    )
    terms = forms.BooleanField(
        error_messages={'required': 'You must accept the terms and conditions'}
    )
    # image_uploads = forms.ImageField(
    #     required=False
    # )


class ContactUsForm(forms.Form):
    fullname = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter your full name',
                'class': 'form-control'
            }
        )
    )
    phone_number = forms.CharField(
        required=False,
        max_length=16,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter your phone number',
                'class': 'form-control'
            }
        )
    )
    email = forms.EmailField(
        max_length=200,
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Enter your E-mail',
                'class': 'form-control'
            }
        )
    )
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Enter message here...',
                'class': 'form-control',
                'rows': 7,
                'cols': 25
            }
        ),
        max_length=2000
    )

    # def clean(self):
    #     cleaned_data = super(ContactForm, self).clean()
    #     fullname = cleaned_data.get('fullname')
    #     phone = cleaned_data.get('phone')
    #     email = cleaned_data.get('email')
    #     address = cleaned_data.get('address')
    #     description = cleaned_data.get('description')
    #     image = cleaned_data.get('image_uploads')
    #
    #     if not fullname and not email and not phone and not address and not description and not image:
    #         raise forms.ValidationError('No empty fields!')
