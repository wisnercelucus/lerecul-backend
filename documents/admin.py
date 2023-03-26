from django.contrib import admin

from .models import Document, RecordDocumentGroup

class DocumentAdmin(admin.ModelAdmin):
    pass

class RecordGroupDocumentAdmin(admin.ModelAdmin):
    pass

admin.site.register(Document, DocumentAdmin)
admin.site.register(RecordDocumentGroup, RecordGroupDocumentAdmin)