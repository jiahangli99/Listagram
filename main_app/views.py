from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
import uuid
import boto3
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Photo


S3_BASE_URL = 'https://s3.us-east-1.amazonaws.com/'
BUCKET = 'instagram-ga'
# Create your views here.

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        error_message = 'invalid credentials - please try again'
    form = UserCreationForm()
    context = {'form': form, 'error': error_message}
    return render(request, 'registration/signup.html', context)

def home(request):
    photos = Photo.objects.all()
    return render(request, 'home.html', {'photos': photos})
@login_required
def posts_index(request):
    photos = Photo.objects.filter(user=request.user)
    return render(request,'posts/index.html', { 'photos': photos})
@login_required
def post_detail(request, photo_id):
    photo = Photo.objects.get(id=photo_id)
    if photo.user_id != request.user.id:
      return redirect('home')
    return render(request, 'posts/detail.html', {
    'photo': photo,
  })
@login_required
def add_photo(request):
    # collect the file asset from the request
    if request.method == "POST":

        photo_file = request.FILES.get('photo-file', None)
        # check if file is present
        if photo_file:
            # create a reference to the s3 service from boto3
            s3 = boto3.client('s3')
            # create a unique identifier for each photo asset
            key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]

            try:
                s3.upload_fileobj(photo_file, BUCKET, key)
                url = f'{S3_BASE_URL}{BUCKET}/{key}'
                name = request.POST.get("name", "")
                user = request.user
                photo = Photo(url=url, name=name, user=user)
                photo.save()
            except Exception as error:
                print('************************')
                print('An error has occured with s3: ')
                print(error)
                print('************************')
        return redirect('home')
    else:
        return render(request, 'main_app/photo_form.html')

# class PostCreate(LoginRequiredMixin, CreateView):
#     model = Photo
#     fields = ('name',)
#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super().form_valid(form)

class PostDelete(LoginRequiredMixin, DeleteView):
    model = Photo
    success_url = '/posts/'

class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Photo
    fields = ('name',)
    template_name = 'main_app/update_form.html'
    success_url = '/'

