from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Eventos, Inscripciones

class FormularioEventos(ModelForm):
    
    participantes = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Sleccione los participantes"
    )
    
    class Meta:
        model = Eventos
        fields = ['nombreEvento', 'descripcion', 'ubicacion', 'fechaCreacion']

        widgets = {
            'nombreEvento': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control'}),
            'fechaCreacion': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }

class FormularioInscripcion(forms.ModelForm):
    class Meta:
        model = Inscripciones
        fields = ['usuario']