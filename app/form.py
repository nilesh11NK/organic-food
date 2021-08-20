from django import forms
from .models import *

class RegForm(forms.ModelForm):
	class Meta:
		model=Registation
		fields="__all__"
