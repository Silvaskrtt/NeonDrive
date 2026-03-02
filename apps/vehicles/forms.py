# forms.py

from django import forms
from .models import Vehicle

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['mark', 'model', 'year', 'car_plate', 'color', 'value', 'status', 'image']
        widgets = {
            'mark': forms.TextInput(attrs={'class': 'w-full bg-slate-700/50 border border-slate-600 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-cyan-500'}),
            'model': forms.TextInput(attrs={'class': 'w-full bg-slate-700/50 border border-slate-600 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-cyan-500'}),
            'year': forms.NumberInput(attrs={'class': 'w-full bg-slate-700/50 border border-slate-600 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-cyan-500'}),
            'car_plate': forms.TextInput(attrs={'class': 'w-full bg-slate-700/50 border border-slate-600 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-cyan-500', 'placeholder': 'ABC-1234'}),
            'color': forms.TextInput(attrs={'class': 'w-full bg-slate-700/50 border border-slate-600 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-cyan-500'}),
            'value': forms.TextInput(attrs={
                'class': 'w-full bg-slate-700/50 border border-slate-600 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-cyan-500',
                'type': 'number',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00'
            }),
            'status': forms.Select(attrs={'class': 'w-full bg-slate-700/50 border border-slate-600 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-cyan-500'}),
            'image': forms.FileInput(attrs={'class': 'w-full bg-slate-700/50 border border-slate-600 rounded-lg px-4 py-3 text-white file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-cyan-600 file:text-white hover:file:bg-cyan-700'}),
        }