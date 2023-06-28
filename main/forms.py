from django.forms import ModelForm, SelectDateWidget, NumberInput, DateInput
from .models import Articulo, Taller

class ArticuloForm(ModelForm):
    
    class Meta:
        model = Articulo
        fields = '__all__'
      
        
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["codigo"].widget.attrs.update(
            {"class": "form-control", 'id':'codigo', 'type':'text'}
        )
        self.fields["nombre"].widget.attrs.update({"class": "form-control", 'id':'nombre', 'type':'text'})
        self.fields["costo"].widget.attrs.update(
            {"class": "form-control", 'id':'costo', 'type':'text'}
        )
        self.fields["cantidad_producida_en_el_mes"].widget.attrs.update(
            {"class": "form-control", 'id':'cantidad_producida_en_el_mes', 'type':'text'}
        )
        self.fields["taller"].widget.attrs.update(
            {"class": "form-select", 'id':'taller', 'type':'text', "placeholder": "Taller"}
        )
    
        self.fields["mes_proceso"].widget.attrs.update(
            {"class": "form-control", "type": "date", 'id':'mes_proceso'}
        )
        self.fields["cantidad_rechazada"].widget.attrs.update(
            {"class": "form-control", 'id':'cantidad_rechazada', 'type':'text'}
        )
