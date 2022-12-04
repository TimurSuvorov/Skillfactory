from django.contrib import admin

from .models import Author, Category, Post, PostCategory, Comment

def nulledrating(modeladmin, request, queryset):
    queryset.update(rating=0)


nulledrating.short_description = 'Обнуление рейтинга постов'


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'rating', 'type', 'cr_time', 'postAuthor')
    list_display_links = ('title', )
    search_fields = ('title', )
    list_editable = ('rating', )
    list_filter = ('postAuthor', 'type', 'cr_time', )
    actions = [nulledrating]


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('author', 'rating', 'postnumber')
    list_filter = ('author', )

class CommentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Comment._meta.get_fields()]


admin.site.register(Author, AuthorAdmin)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory)
admin.site.register(Comment, CommentAdmin)

