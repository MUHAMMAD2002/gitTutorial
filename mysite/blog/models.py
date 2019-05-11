from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User


class PublishedManager(models.Manager):
   def get_queryset(self):
      return super(PublishedManager, self).get_queryset().filter(status='published')


class Post(models.Model):
   STATUS_CHOICES = (
      ('draft', 'Draft'),
      ('published', 'Published'),
   )

   title = models.CharField(max_length=250)
   # Title with max length of 250 symbols

   slug = models.SlugField(max_length=250, unique_for_date='publish')
   # Slug with max length of 250 sumbols, and that connects to 'publish' Column

   author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
   # This field is a foreing-key(внешним-ключом). it defines a many-to-one(многи-к-одному) relationship

   body = models.TextField()
   # Text

   publish = models.DateTimeField(default=timezone.now)
   # You can think of it as a timezone-aware version of the standard Python datetime.now method.

   created = models.DateTimeField(auto_now_add=True)
   # This datetime indicates when the post was created.
   # Since we are using auto_now_add here, the date will be saved automatically when creating an object.

   updated = models.DateTimeField(auto_now=True)
   # This datetime indicates the last time the post was updated.
   # Since we are using auto_now here, the date will be updated automatically when saving an object.

   status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

   class Meta:
      ordering = ('-publish',)
   # The Meta class inside the model contains metadata. We tell Django to sort results in the 
   # publish field in descending order by default when we query the database.
   # We specify descending order using the negative prefix. By doing so, posts published recently 
   # will appear first.

   def __str__(self):
      return self.title
   # The __str__() method is the default human-readable representation of the object.
   # Django will use it in many places, such as the administration site.

   objects = models.Manager() # The default manager.
   published = PublishedManager() # Our custom manager.
   
   def get_absolute_url(self):
      return reverse('blog:post_detail', args=[self.publish.year,
                                               self.publish.month,
                                               self.publish.day,
                                               self.slug])