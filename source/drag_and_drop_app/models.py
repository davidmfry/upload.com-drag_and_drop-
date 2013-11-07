from django.db import models

class UploadModel(models.Model):
    first_name = models.CharField(max_length = 250)
    last_name = models.CharField(max_length = 250)
    email = models.EmailField(max_length = 250)
    phone = models.CharField(max_length = 250)
    message = models.TextField()
    file_name = models.CharField(max_length = 500)
    dirname = models.CharField(max_length = 500)
    checked_by = models.CharField(max_length= 200)
    has_been_checked = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add = True, auto_now = False)
    
    def __unicode__(self):
        return self.first_name + ", " + self.last_name + "| " + self.email
