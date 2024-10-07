from django.db import models

class UrlData(models.Model):
    url = models.CharField(max_length=2048)
    slug = models.CharField(max_length=15)
    def foo(self):
        return UrlData.objects.all()
    class Meta:
        app_label = 'url_short'

def __str__(self):
        return f"Short Url for: {self.url} is {self.slug}"



