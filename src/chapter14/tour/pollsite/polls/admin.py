# polls admin.py
from pollsite.polls.models import Poll, Choice
from django.contrib import admin

class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3

class PollAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    search_fields = ['question']
    list_filter = ['pub_date']
    list_display = ['question', 'pub_date']
    

admin.site.register(Poll, PollAdmin)
