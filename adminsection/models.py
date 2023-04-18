from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from ckeditor.fields import RichTextField


# Model for categories
class CategoryModel(models.Model):
    category_name = models.CharField(max_length=200,null=True,blank=True)
    category_keywords = models.TextField(max_length=1000, null=True, blank=True)
    category_description = models.CharField(max_length=160, null=True, blank=True)
    category_author = models.CharField(max_length=160, null=True, blank=True)
    category_slug = models.SlugField(max_length=255,unique=True,blank=True,null=True)
    added_date = models.DateTimeField(auto_now_add=True)

    def generateSlug(self):
        if not self.id and not self.category_slug:
            slug = slugify(self.category_name)
            slug_exists = True
            counter = 1
            self.category_slug = slug
            while slug_exists:
                try:
                    slug_exits = CategoryModel.objects.get(category_slug=slug)
                    if slug_exits:
                        slug = self.category_slug + '-' + str(counter)
                        counter += 1
                except CategoryModel.DoesNotExist:
                    self.category_slug = slug
                    break


    def save(self,*args,**kwargs):
        self.generateSlug()
        super(CategoryModel, self).save(*args, **kwargs)

    # Getting category slug for sitemap - SEO related method
    def get_absolute_url(self):
        return f"/{self.category_slug}/"

    class Meta:
        db_table = "categorymodel"


# Model for articles
class ArticlesModel(models.Model):
    Category = models.ForeignKey(CategoryModel,verbose_name="category",on_delete=models.CASCADE)
    article_title = models.CharField(max_length=200,null=True,blank=True)
    article_keywords = models.TextField(max_length=1000, null=True, blank=True)
    artilce_meta_des = models.CharField(max_length=160,null=True,blank=True)
    article_author = models.CharField(max_length=100, null=True, blank=True)
    article_content = RichTextField(null=True,blank=True)
    article_image = models.ImageField(upload_to="ArticlesImages",unique=True,null=True,blank=True)
    article_slug = models.SlugField(max_length=255,null=True,blank=True,unique=True)
    updated_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(auto_now_add=True)

    def generateSlug(self):
        if not self.id and not self.article_slug:
            slug = slugify(self.article_title)
            slug_exists = True
            counter = 1
            self.article_slug = slug
            while slug_exists:
                try:
                    slug_exits = ArticlesModel.objects.get(article_slug=slug)
                    if slug_exits:
                        slug = self.article_slug + '-' + str(counter)
                        counter += 1
                except ArticlesModel.DoesNotExist:
                    self.article_slug = slug
                    break

    def save(self,*args,**kwargs):
        self.generateSlug()
        super(ArticlesModel, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return f"/{self.Category.category_slug}/{self.article_slug}/"

    class Meta:
        db_table = "articlesmodel"


    # Overriding delete method The reason is "If we removed this method then on article updating
    # the old image will be present in the directory. So, that's why we did this. In VU & in any other
    # Pakistani university they don't teach these things. They are just making money & destroying the young generation
    # Which is the future of Pakistan.
    def delete(self,*args,**kwargs):
        self.article_image.delete()
        return super().delete(*args,**kwargs)


# Model for notifications for both admin and users
class NotificationModel(models.Model):
    title = models.CharField(max_length=200,null=True,blank=True)
    message = models.TextField(max_length=1500,null=True,blank=True)
    status = models.CharField(max_length=20,null=True,blank=True,default="Unread")
    generated_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "notificationmodel"
