from django import forms
from .models import Hood, Status, Bio, Business
from django.contrib.auth.models import User

class BioForm(forms.ModelForm):
    class Meta:
        model = Bio
        fields = '__all__'
        exclude = ['user']

class HoodForm(forms.ModelForm):
    class Meta:
        model = Hood
        fields = ('name',)
        
class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = '__all__'
        exclude = ['date_added', 'user']

class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = '__all__'
        exclude = ['hood','user','date_posted']

class EditUser(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')