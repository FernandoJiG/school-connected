from django.forms import ModelForm
from .models import Room
from django.contrib.auth.models import User

class RoomForm(ModelForm):
    class Meta:
        model = Room
        exclude=["participants", "host"]
        #fields='__all__'

class UserForm(ModelForm):
    class Meta:
        model=User
        fields=['username', 'email']