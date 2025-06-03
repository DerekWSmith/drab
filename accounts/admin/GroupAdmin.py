from django.contrib import admin
from accounts.models import Group, GroupMembership

class GroupMembershipInline(admin.TabularInline):
    model = GroupMembership
    extra = 0
    fields = ('user', 'start_date', 'expiry_date', 'is_active', 'last_read', 'notes')
    autocomplete_fields = ('user',)

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator', 'is_auto', 'created_at')
    search_fields = ('name', 'creator__email')
    list_filter = ('is_auto',)
    inlines = [GroupMembershipInline]

@admin.register(GroupMembership)
class GroupMembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'group', 'is_active', 'start_date', 'expiry_date', 'last_read')
    search_fields = ('user__email', 'group__name')
    list_filter = ('is_active', 'group')
    autocomplete_fields = ('user', 'group')