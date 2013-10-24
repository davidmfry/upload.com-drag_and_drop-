import os, sys, shutil
from tempfile import mkstemp
import tempfile
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
    temp_file = make_temp_file(files)
    shutil.move(temp_file, sys.path[0] + "/PROJECTS/" + files.name)
            
    
    return HttpResponse("Sucess!")