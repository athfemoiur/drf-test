from django.contrib import admin

from post.models import UserPostScore, Post


class UserScoreInline(admin.TabularInline):
    model = UserPostScore
    extra = 0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'body')
    inlines = [UserScoreInline]
