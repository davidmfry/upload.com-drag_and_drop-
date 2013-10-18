from django.db import models

class UploadModel(models.Model):
    first_name = models.CharField(max_length = 250)
    last_name = models.CharField(max_length = 250)
    email = models.EmailField(max_length = 250)
    phone = models.CharField(max_length = 250)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add = True, auto_now = False)
    
    def __unicode__(self):
        return self.first_name + ", " + self.last_name + "| " + self.email
