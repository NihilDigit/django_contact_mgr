from django import forms
from .models import Contact, Todo


class ContactForm(forms.ModelForm):
    delete_avatar = forms.BooleanField(required=False, label='删除头像')

    class Meta:
        model = Contact
        fields = ['ct_name', 'ct_phone', 'email', 'gender', 'birthday', 'avatar', 'address']
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
            'avatar': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['event', 'time']
        widgets = {
            'time': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M')
        }