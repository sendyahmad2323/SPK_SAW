from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Criteria, Framework, FrameworkScore

class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})

class CriteriaForm(forms.ModelForm):
    class Meta:
        model = Criteria
        fields = ['name', 'weight', 'attribute']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Masukkan nama kriteria'
            }),
            'weight': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'max': '1',
                'placeholder': '0.00'
            }),
            'attribute': forms.Select(attrs={
                'class': 'form-select'
            }),
        }

    def clean_weight(self):
        weight = self.cleaned_data.get('weight')
        if weight is not None and (weight <= 0 or weight > 1):
            raise forms.ValidationError('Bobot harus antara 0.01 sampai 1.0')
        return weight

        
class FrameworkForm(forms.ModelForm):
    class Meta:
        model = Framework
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nama framework (contoh: Django, Flask, FastAPI)'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Deskripsi singkat tentang framework ini...'
            }),
        }
        

    def clean(self):
        cleaned_data = super().clean()
        for field in ['performa', 'skalabilitas', 'komunitas', 'kemudahan_belajar', 'pemeliharaan']:
            value = cleaned_data.get(field)
            if value is not None and (value < 1 or value > 10):
                self.add_error(field, 'Nilai harus antara 1 dan 10')

class FrameworkScoreForm(forms.ModelForm):
    class Meta:
        model = FrameworkScore
        fields = ['framework', 'criteria', 'value']
        widgets = {
            'framework': forms.Select(attrs={'class': 'form-select'}),
            'criteria': forms.Select(attrs={'class': 'form-select'}),
            'value': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
        }


class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(
        label='Pilih file CSV',
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.csv'
        }),
        help_text='Format file: criteria.csv, frameworks.csv, atau scores.csv'
    )

    def clean_csv_file(self):
        file = self.cleaned_data.get('csv_file')
        if file:
            if not file.name.endswith('.csv'):
                raise forms.ValidationError('File harus berformat CSV (.csv)')
            if file.size > 5 * 1024 * 1024:
                raise forms.ValidationError('Ukuran file maksimal 5MB')
        return file
