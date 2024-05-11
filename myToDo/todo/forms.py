from django.forms import ModelForm
from .models import ToDo
class ToDoForms(ModelForm):

    class Meta:
        model = ToDo
        fields = ['title', 'description', 'important']