from django.shortcuts import render
import json
from django.core.files.storage import FileSystemStorage
from shop.forms import FileForm
from django.http import JsonResponse
from django.http import HttpResponse
from shop.models import *
#json_data = '{"hello": "world", "foo": "bar"}' 

#data = json.loads(json_data)
# Create your views here.
'''
def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)

response_data = {}
response_data['result'] = 'error'
response_data['message'] = 'Some error message'
'''
def model_form_upload(request):
    response_data = {}
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            model_instance = form.save(commit=False)
            model_instance.save()
            bucket = Bucket(files=model_instance)
            bucket.save()
            bucket.name="some_name"
            bucket.save()
            response_data['bucket_id'] = bucket.id
            response_data['message'] = "file upload successful"
        else:
            response_data['message'] = 'Some error message'

    return JsonResponse(response_data)

        