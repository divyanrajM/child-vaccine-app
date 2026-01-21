from django.contrib import admin
from .models import Child, Vaccine, VaccinationRecord


@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
    list_display = ['child_name', 'rch_number', 'parent_number', 'age_display', 'sex', 'created_at']
    search_fields = ['child_name', 'rch_number', 'parent_number']
    list_filter = ['sex', 'created_at']
    ordering = ['-created_at']


@admin.register(Vaccine)
class VaccineAdmin(admin.ModelAdmin):
    list_display = ['name', 'recommended_age_months', 'description']
    search_fields = ['name']
    ordering = ['recommended_age_months']


@admin.register(VaccinationRecord)
class VaccinationRecordAdmin(admin.ModelAdmin):
    list_display = ['child', 'vaccine', 'scheduled_date', 'administered_date', 'status']
    list_filter = ['status', 'vaccine']
    search_fields = ['child__child_name', 'vaccine__name']
    ordering = ['scheduled_date']
