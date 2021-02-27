from django.contrib import admin
from scraping.models import City, Language, Vacancy, Error, Url




class VacancyAdmin(admin.ModelAdmin):

    fields = ('url', 'title', 'company', 'description', 'city', 'language', 'timestamp',)
    readonly_fields = ('timestamp',)



class ErrorAdmin(admin.ModelAdmin):

    fields = ('timestamp', 'datestamp', 'data',)
    readonly_fields = ('timestamp', 'datestamp',)




admin.site.register(City)
admin.site.register(Language)
admin.site.register(Vacancy, VacancyAdmin)
admin.site.register(Error, ErrorAdmin)
admin.site.register(Url)
