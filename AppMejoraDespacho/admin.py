from django.contrib import admin
from file_resubmit.admin import AdminResubmitMixin
from .models import Ordenes

class OrdenesAdmin(AdminResubmitMixin, admin.ModelAdmin):
    pass

admin.site.register(Ordenes, OrdenesAdmin)