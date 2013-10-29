import os, sys, shutil
from tempfile import mkstemp
import tempfile
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from django.shortcuts import render_to_response, RequestContext, render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .models import UploadModel
from .forms import UploadInfoForm

#Global Variables

FORM_CREATED_USER_PATH = ''

# creats a directory structure base on the give from data
def make_dir(form_data):
    #creates the directory path from the from data
    dirname = sys.path[0] + "/PROJECTS/" + form_data['first_name'] + "_" + form_data['last_name'] + "/"
    
    # check if the directory exisits, it not it creats it.
    
    if not os.path.exists(dirname):
        os.makedirs(dirname)
        return dirname
    else:
        return dirname
    
def make_temp_file(tmp_file):
    tmp_upload = tempfile.mkstemp()
    new_file = os.fdopen(tmp_upload[0], 'w')
    new_file.write(tmp_file.read())
    new_file.close()
    filepath = tmp_upload[1]
    return filepath
    

def uploadform(request):
    
    form = UploadInfoForm(request.POST)
    
    if form.is_valid():
        
        form_data = form.cleaned_data
        
        # Directory created
        #UploadModel.objects.update(dirname=make_dir(form_data))
        #UploadModel.dirname = make_dir(form_data)
        
        # Database Create and Update
        # Checks if the form and model/database first name and last name matach, if it does it updates the recored with new info
        if UploadModel.objects.filter(first_name__contains=form_data['first_name']).filter(last_name__contains=form_data['last_name']):
            
            db_field = UploadModel.objects.filter(first_name__contains=form_data['first_name']).filter(last_name__contains=form_data['last_name'])
            
            db_field.update(
                email=form_data['email'],
                phone=form_data['phone'],
                message=form_data['message'])
            return HttpResponseRedirect("/upload")
        else:
            # creats a new record in the database from the user input on the form
            new_upload_form = form.save(commit=False or None)
            new_upload_form.dirname = make_dir(form_data)
            new_upload_form.save()
            return HttpResponseRedirect("/upload")
      
    return render(request, 'upload/form.html', locals())

def upload(request): 
    return render(request, 'upload/upload.html', locals())

def upload_files(request):

    files = request.FILES['upl']                                    # gets the inmemory file
    # A function that makes the file in memory into a temp file 
    temp_file = make_temp_file(files)
    #dest_dir = sys.path[0] + "/PROJECTS/" + files.name
    dest_dir = str(UploadModel.objects.latest('timestamp').dirname) + files.name
    shutil.move(temp_file, dest_dir)
 
    #path = default_storage.save('PROJECTS/' + files.name, ContentFile(files.read()))
    #tmp_file = os.path.join(settings.MEDIA_ROOT, path)



    return HttpResponse(sys.path[0] + "/PROJECTS/")


    #'{0[parent_dir]}/PROJECTS/{1[file_name]}'.format({'parent_dir': sys.path[0], "file_name":files.name}


def master(request):
    db = UploadModel.objects.all()
    return render(request, 'upload/master.html', {"db": db})