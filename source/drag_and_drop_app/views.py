# python imports
import os, sys, shutil
import tempfile

from tempfile                   import mkstemp

# Django imports
from django.core.files.storage  import default_storage
from django.core.files.base     import ContentFile
from django.core.urlresolvers   import reverse
from django.conf                import settings
from django.shortcuts           import render_to_response, RequestContext, render
from django.http                import HttpResponse
from django.http                import HttpResponseRedirect
from .models                    import UploadModel
from .forms                     import UploadInfoForm, MasterResponseForm

# third party imports
import mandrill

#Global Variables

FORM_CREATED_USER_PATH = ''

# creats a directory structure base on the give from data
def make_dir(form_data):
    #creates the directory path from the from data
    home_path = sys.path[0]
    dirname = home_path[0:-6] + "static/" + "static/" "media/" + "PROJECTS/" + form_data['first_name'] + "_" + form_data['last_name'] + "/"
    
    # check if the directory exisits, it not it creats it.
    
    if not os.path.exists(dirname):
        os.makedirs(dirname)
        return dirname
    else:
        return dirname
    
def make_temp_file(tmp_file):
    tmp_upload  = tempfile.mkstemp()
    new_file    = os.fdopen(tmp_upload[0], 'w')
    
    new_file.write(tmp_file.read())
    new_file.close()
    
    filepath    = tmp_upload[1]
    return filepath

def send_email(api_key, from_name, from_email, to_email, to_name, subject, message ):
    try:
        # You need an account with mandrill to get your api key
        mandrill_client = mandrill.Mandrill(api_key)
        
        # Creating the email message
        message = { 'from_name' : from_name,
                    'from_email': 'message.' + from_email,
                    'to':[{ 'email': to_email,
                            'name' : to_name,
                            }],
                    'subject': subject,
                    'text': message,
                     }
        result = mandrill_client.messages.send(message=message, async=False, ip_pool='Main Pool')
    except mandrill.Error, e:
        # Mandrill errors are thrown as exceptions
        print 'A mandrill error occurred: %s - %s' % (e.__class__, e)
        # A mandrill error occurred: <class 'mandrill.UnknownSubaccountError'> - No subaccount exists with the id 'customer-123'    
        raise

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
                checked_by='',
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
    file_names = []
    files = request.FILES['upl']                                    # gets the inmemory file

    url_id = split_url(str(request.path))
    temp_file = make_temp_file(files)
    dest_dir = str(UploadModel.objects.get(id=url_id[2]).dirname) + files.name
    shutil.move(temp_file, dest_dir)

    UploadModel.objects.filter(id__contains=url_id[2]).update(file_name=files.name)
    
    return HttpResponse(UploadModel.objects.get(id=url_id[2]).dirname)

def master(request):
    db = UploadModel.objects
    form = MasterResponseForm(request.POST)
    site_path = str(request.path)[1:7]
    the_request = request
    sys_path = sys.path[0]
    
    return render(request, 'upload/master.html', {"db": db.all(), "sys_path":sys_path[0:-6], "site_path":site_path, "form": form, "the_request":the_request })

def master_checked(request):
    
    

    db = UploadModel.objects
    form = MasterResponseForm(request.POST)
    data = request.POST
    
    mandrill_api_key = '-gwymhejJEt5AK57eX3hEA'
    from_name = 'Upload Web App'
    from_email = 'david.fry.tv@gmail.com'
    subject = 'Testing replay_message from form'
    
    client_name = db.get(id=request.POST["id"]).first_name, db.get(id=request.POST["id"]).last_name
    client_email = db.get(id=request.POST["id"]).email

    default_replay_message = "This is just a test!"

    # default message is sent if nothing is inputed in the message field
    if data["replay_message"] == '':
        send_email(mandrill_api_key, from_name, from_email, client_email, client_name, subject, default_replay_message )
        #return HttpResponse("The message is empty: Default message sent")
    else:
        send_email(mandrill_api_key, from_name, from_email, client_email, client_name, subject, data["replay_message"] )


    db.filter(id=request.POST["id"]).update(checked_by=request.POST["checked_by"])
    db.filter(id=request.POST["id"]).update(has_been_checked=True)

    url = reverse('master')
    return HttpResponseRedirect(url)
    #return HttpResponse(request.POST["checked_by"])
























