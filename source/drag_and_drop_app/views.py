import os, sys, shutil
from tempfile import mkstemp
import tempfile
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.urlresolvers import reverse
from django.conf import settings
from django.shortcuts import render_to_response, RequestContext, render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .models import UploadModel
from .forms import UploadInfoForm, MasterResponseForm

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

def split_url(the_url):
    split_list = the_url.split('/')
    return split_list

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
                message=form_data['message'],
                dirname=make_dir(form_data),
                has_been_checked=False)

            url = reverse('upload', kwargs={'user_id': db_field[0].id})
            return HttpResponseRedirect(url)
        else:
            # creats a new record in the database from the user input on the form
            new_upload_form = form.save(commit=False or None)
            new_upload_form.dirname = make_dir(form_data)
            new_upload_form.has_been_checked = False
            new_upload_form.save()
            url = reverse('upload', kwargs={'user_id': new_upload_form.id})
            return HttpResponseRedirect(url)
      
    return render(request, 'upload/form.html', locals())

def upload(request, user_id):

    return render(request, 'upload/upload.html', locals())

def upload_files(request, user_id):

    files = request.FILES['upl']                                    # gets the inmemory file
    url_id = split_url(str(request.path))
    #for item in files:
    #    UploadModel.objects.filter(id__contains=url_id[2]).update(file_name=files.name)
    # A function that makes the file in memory into a temp file 
    temp_file = make_temp_file(files)
    #dest_dir = sys.path[0] + "/PROJECTS/" + files.name
    dest_dir = str(UploadModel.objects.get(id=url_id[2]).dirname) + files.name
    shutil.move(temp_file, dest_dir)
 
    #path = default_storage.save('PROJECTS/' + files.name, ContentFile(files.read()))
    #tmp_file = os.path.join(settings.MEDIA_ROOT, path)



    return HttpResponse(UploadModel.objects.get(id=url_id[2]).dirname)


    #'{0[parent_dir]}/PROJECTS/{1[file_name]}'.format({'parent_dir': sys.path[0], "file_name":files.name}



def master(request):
    db = UploadModel.objects
    form = MasterResponseForm(request.POST)
    site_path = str(request.path)[1:7]
    
    return render(request, 'upload/master.html', {"db": db.all(), "site_path":site_path, "form": form})

def master_checked(request):
    
    db = UploadModel.objects
    #if request.is_ajax():
    db.filter(id=request.POST["id"]).update(has_been_checked=True)
        #form = MasterResponseForm(request.POST)
        #client_id = db.get(id=request.POST["id"]).has_been_checked
        
        
        #if form.is_valid():
            #form_data = form.cleaned_data
            #db.get(id=request.POST["id"]).update(has_been_checked=True)
            #form.has_been_checked = True
            #form.save(commit=False or None)
    url = reverse('master')
    return HttpResponseRedirect(url)

























