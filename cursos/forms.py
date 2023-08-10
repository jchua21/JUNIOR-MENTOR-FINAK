from django import forms
from .models import Curso
from .snippets import choices

class CursoCreateForm(forms.ModelForm):
    title = forms.CharField(label="Título", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el título'}))
    categories = forms.CharField(label="Categorías", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Categorías separadas por coma. Ejemplo: chino, tailandés'}))
    image = forms.ImageField(label="Imagen", widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    location = forms.CharField(label="Ubicación", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la ubicación'}))
    price = forms.IntegerField(label="Precio", widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el precio'}))
    details = forms.CharField(label="Detalles", widget=forms.Textarea(attrs={'class': 'form-control'}))

    class Meta:
        model = Curso
        fields = ['title', 'image', 'categories', 'location', 'price', 'details']

    lecciones = forms.CharField(widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['lecciones'].widget = forms.HiddenInput()


