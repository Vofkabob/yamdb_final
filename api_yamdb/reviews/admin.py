from django.contrib import admin

from .models import Review, Comment


class CustomReviewAdmin(admin.ModelAdmin):
    list_display = ('title',
                    'pub_date',
                    'author',
                    'text',
                    'score')
    search_fields = ('title',
                     'author',
                     'text')
    list_filter = ('pub_date',
                   'score')
    empty_value_display = '-пусто-'


class CustomCommentAdmin(admin.ModelAdmin):
    list_display = ('review',
                    'pub_date',
                    'author',
                    'text')
    search_fields = ('review',
                     'author',
                     'text')
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


admin.site.register(Review, CustomReviewAdmin)
admin.site.register(Comment, CustomCommentAdmin)
