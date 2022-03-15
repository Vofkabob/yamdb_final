from django.contrib import admin

from .models import Category, Genre, Title


class CustomBaseAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'slug')
    search_fields = ('name',
                     'slug')


class CustomTitleAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'year',
                    'genres_list',
                    'category',
                    'description')
    search_fields = ('name',
                     'genre',
                     'category',
                     'description')
    list_filter = ('year',)

    def genres_list(self, obj):
        return ",\n".join(obj.genre.values_list('name', flat=True).all())


admin.site.register(Category, CustomBaseAdmin)
admin.site.register(Genre, CustomBaseAdmin)
admin.site.register(Title, CustomTitleAdmin)
