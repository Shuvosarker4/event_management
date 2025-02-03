from django import forms
from events.models import Event,Category,Participant
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django import forms
import re

class StyleFormMixin:
    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.apply_style_widgets()

    default_classes ="border-2 my-2 w-full p-3 rounded-lg shadow-sm "
    def apply_style_widgets(self):
        for field_name,field in self.fields.items():
            if isinstance(field.widget,forms.TextInput):
                field.widget.attrs.update({
                    'class':self.default_classes,
                    'placeholder':f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget,forms.Textarea):
                field.widget.attrs.update({
                    'class':self.default_classes,
                    'placeholder':f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget, forms.SelectDateWidget):
                field.widget.attrs.update({
                    'class': "border-2 my-2 border-gray-300 p-3 rounded-lg shadow-sm focus:outline-none focus:border-rose-500 focus:ring-rose-500"
                })
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    'class': "space-y-4"
                })
            elif isinstance(field.widget,forms.PasswordInput):
                field.widget.attrs.update({
                    'class':self.default_classes,
                    'placeholder':"Enter your password"
                })
            elif isinstance(field.widget,forms.EmailInput):
                field.widget.attrs.update({
                    'class':self.default_classes,
                    'placeholder':"Enter your email address"
                })

class CategoryModelForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name','description']
        labels = {
            'name': 'Event Name',
            'description': 'Description',
        }
        widgets ={
            'name': forms.TextInput(attrs={
                'class': 'p-2 border-blue-500 rounded', 
                'placeholder': 'Enter Category Name',
            }),
            'description': forms.Textarea(attrs={
                'class': 'p-2 border-blue-500 rounded', 
                'placeholder': 'Enter Category Description',
            })
        }
        

class ParticipantModelForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['name','email']
        labels = {
            'name': 'Participant Name',
            'email': 'Email Address',
        }
        widgets ={
            'name': forms.TextInput(attrs={
                'class': 'p-2 border-blue-500 rounded', 
                'placeholder': 'Enter Participants Name',
            }),
            'email': forms.TextInput(attrs={
                'class': 'p-2',
                'placeholder': 'Enter Email Address',
            })
        }
       

class EventModelForm(forms.ModelForm):
    class Meta:
        model = Event
        fields=['name','description','date','time','location','category','participant']
        labels = {
            'name': 'Event Name',
            'description': 'Description',
            'date': 'Event Date',
            'time': 'Event Time',
            'location': 'Location',
            'category': 'Category',
            'participant': 'Participants',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'p-2',
                'placeholder': 'Enter Event Name',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Event Description',
                'rows': 4,
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time',
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control p-2',
                'placeholder': 'Enter Event Location',
            }),
            'category': forms.Select(attrs={
                'class': 'form-select',
            }),
            'participant': forms.CheckboxSelectMultiple(attrs={
                'class': 'form-control',
            }),
        }




class CustomRegisterForm(StyleFormMixin,forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name', 'password','confirm_password']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_exists = User.objects.filter(email=email)
        if email_exists:
            raise forms.ValidationError("Email address already exits!")
        return email
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        errors = []
        if len(password)<8:
            errors.append('Password must be at least 8 character long!')
        if not re.search(r'[A-Z]',password):
            errors.append('Password must have one Uppercase letter')
        if not re.search(r'[a-z]',password):
            errors.append('Password must have one Lowercase letter')
        if not re.search(r'[0-9]',password):
            errors.append('Password must have one number')
        if not re.search(r'[@#$%^&+=]',password):
            errors.append('Password must have one Special Character')
        if errors:
            raise forms.ValidationError(errors)
        return password
    
class LoginForm(StyleFormMixin,AuthenticationForm):
    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)