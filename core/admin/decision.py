from django.contrib import admin
from core.models.Decision import Decision

@admin.register(Decision)
class DecisionAdmin(admin.ModelAdmin):
    list_display = ('id', 'resolution', 'adopted_date', 'quorum', 'recommended_outcome_display')
    readonly_fields = ('recommended_outcome_display',)
    filter_horizontal = ('veto_group', 'mandatory_voters')

    def recommended_outcome_display(self, obj):
        return obj.recommended_outcome
    recommended_outcome_display.short_description = 'Recommended Outcome'
