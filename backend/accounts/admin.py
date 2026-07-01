from django.contrib import admin

from .models import DataRequest


@admin.register(DataRequest)
class DataRequestAdmin(admin.ModelAdmin):
    """Consultation des traces d'export RGPD (créées uniquement par l'API)."""

    list_display = ["user", "status", "format", "requested_at", "response_at", "export_hash"]
    list_filter = ["status", "format"]
    search_fields = ["user__username", "user__email", "export_hash"]
    readonly_fields = [f.name for f in DataRequest._meta.fields]

    def has_add_permission(self, request) -> bool:
        return False  # jamais créée manuellement, uniquement via l'export
