from django.forms import ModelForm
from .models import Room

class RoomForm(ModelForm):
    class Meta:
        model = Room
        exclude=["participants", "host"]
        #fields='__all__'