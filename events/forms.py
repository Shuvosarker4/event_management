from django import forms
from events.models import Event,Category,Participant

class CategoryModelForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name','description']


class ParticipantModelForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['name','email']

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