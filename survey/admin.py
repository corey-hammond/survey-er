from django.contrib import admin
from .models import Question, Choice

admin.site.site_header = 'Survey-er Admin'
admin.site.site_title = 'Survey-er Admin Area'
admin.site.index_title = 'Welcome to the Survey-er Admin Area'

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields': ['question_text']}), ('Date Information', {'fields': ['pub_date'], 'classes': ['collapse']}),]
    inlines = [ChoiceInline]

admin.site.register(Question, QuestionAdmin)
