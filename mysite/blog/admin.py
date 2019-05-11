from django.contrib import admin
from .models import Post

#admin.site.register(Post)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
   list_display = ('title', 'slug', 'author', 'publish', 'status')
   list_filter = ('status', 'created', 'updated')
   search_fields = ('title', 'body')
   date_hierarchy = 'publish'
   ordering = ('status', 'publish')

   prepopulated_fields = {'slug':('title',)}
   raw_id_fields = ('author',)