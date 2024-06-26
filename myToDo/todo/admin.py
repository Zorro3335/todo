from django.contrib import admin
from .models import ToDo
# Register your models here.


class ToDoAdmin(admin.ModelAdmin):
    readonly_fields = ('create_date',)


admin.site.register(ToDo, ToDoAdmin)