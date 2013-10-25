import os, sys, shutil
from tempfile import mkstemp
import tempfile
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from django.shortcuts import render_to_response, RequestContext
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .models import UploadModel
from .forms import UploadInfoForm

# creats a directory structure base on the give from data
def make_dir(form_data):
    #creates the directory path from the from data
    dirname = "PROJECTS/" + form_data['first_name'] + "_" + form_data['last_name'] + "/"
    
    # check if the directory exisits, it not it creats it.
    
    if not os.path.exists(dirname):
        os.makedirs(dirname)
        return dirname
    else:
        return dirname
    
def make_temp_file(tmp_file):
    tmp_upload = tempfile.mkstemp()
    new_file = os.fdopen(tmp_upload[0], 'w')
    new_file.write(tmp_file.read(512))
    new_file.close()
    filepath = tmp_upload[1]
    return filepath
    

def uploadform(request):
    form = UploadInfoForm(request.POST)
    
    if form.is_valid():
        
        form_data = form.cleaned_data
        
        # Directory created
        make_dir(form_data)
        
        # Database Create and Update
        # Checks if the form and model/database first name and last name matach, if it does it updates the recored with new info
        if UploadModel.objects.filter(first_name__contains=form_data['first_name']).filter(last_name__contains=form_data['last_name']):
            
            UploadModel.objects.all().update(
                email=form_data['email'],
                phone=form_data['phone'],
                message=form_data['message'])
        else:
            # creats a new record in the database from the user input on the form
            new_upload_form = form.save(commit=False or None)
            new_upload_form.save()
        
    return render_to_response('upload/form.html', locals(), context_instance = RequestContext(request))

def upload(request):
    
    return render_to_response('upload/upload.html', locals(), context_instance = RequestContext(request))

def upload_files(request):

    files = request.FILES['upl']                                    # gets the inmemory file
    # A function that makes the file in memory into a temp file 
    #temp_file = make_temp_file(files)
    dst_dir = sys.path[0] + "/PROJECTS/"
    #shutil.move(files, dst_dir)
    #with open(files, 'w') as uploaded_file:
    #    uploaded_file.write(dst_dir + files.name)        
    path = default_storage.save('PROJECTS/' + files.name, ContentFile(files.read()))
    tmp_file = os.path.join(settings.MEDIA_ROOT, path)


    return HttpResponse(str(tmp_file))


    #'{0[parent_dir]}/PROJECTS/{1[file_name]}'.format({'parent_dir': sys.path[0], "file_name":files.name}