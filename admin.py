from django.contrib import admin
from . import models
from .models import Clone, SequencedClone

class CloneAdmin(admin.ModelAdmin):
    list_display = ("name", "get_accessions")


class SequencedCloneAdmin(admin.ModelAdmin):
    list_display = ("clonename", "accession", "libabbr", "phase", "clonestate", "seqlen", "chrom")
    list_filter = ("libabbr", "phase", "clonestate", "chrom")
    search_fields = ("clonename", "accession")


admin.site.register(Clone, CloneAdmin)
admin.site.register(SequencedClone, SequencedCloneAdmin)
