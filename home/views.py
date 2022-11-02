from django.shortcuts import get_object_or_404, redirect, render
from .models import *
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.views import View
from django.forms import modelformset_factory
from django.template.loader import render_to_string
from django.db.models import Q

def index(request):
    images = Image.objects.all()
    categories = Category.objects.all()
    context = {
        'images': images,
        'categories': categories,
    }
    return render(request, 'home.html', context)

def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    
    context = {
        'image': image,
    }

    return render(request, 'home/image_detail.html', context)

def blog(request):
    category = request.GET.get('category')
    if category == None:
        images = Image.objects.all()
    else:
        images = Image.objects.filter(category__name=category)
    # images = Image.objects.all()
    categories = Category.objects.all()

    query = request.GET.get('q')
    if query:
        images = Image.objects.filter(
            Q(title__icontains=query)|
            Q(author__username=query)
        )
    context = {
        'images': images,
        'categories': categories,
    }
    return render(request, 'blog.html', context)

def addPhoto(request):
    categories = Category.objects.all()
    
    if request.method == 'POST':
        data = request.POST
        image = request.FILES.get('image')
        
        if data['category'] != 'none':
            category = Category.objects.get(id=data['category'])
        elif data['category_new'] != '':
            category, created = Category.objects.get_or_create(name=data['category_new'])
        else:
            category = None
            
        image = Image.objects.create(
            author=request.user,
            title=data['title'],
            category=category,
            description=data['description'],
            image=image,
        )
        
        return redirect('index')
    
    context = {
        'categories': categories,
    }
    return render(request, 'home/add-photo.html', context)

# user login
def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return HttpResponse('User is not Active')
            else:
                return HttpResponse('User is None')
    else:
        form = UserLoginForm()
    context = {
        'form': form,
    }
        
    return render(request, 'home/signin.html', context)

# user logout
def user_logout(request):
    logout(request)
    return redirect('index')

# user register
def signup(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            return redirect('signin')
    else:
        form = UserRegistrationForm()
    context = {
        'form': form,
    }
        
    return render(request, 'home/signup.html', context)



def dashboard(request, id):
    profile = Profile.objects.get(id=id)
    user = profile.user
    images = Image.objects.filter(author=user).order_by('pub_date')
   
    context = {
        'profile': profile,
        'images': images,
        'user': user,
    }
    return render(request, 'home/dashboard.html', context)

def profile_info(request, id):
    profile = Profile.objects.get(id=id)
    user = profile.user
    images = Image.objects.filter(author=user).order_by('pub_date')
   
    context = {
        'profile': profile,
        'images': images,
        'user': user,
    }
    return render(request, 'home/profile_info.html', context)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserEditForm(
            data=request.POST or None, instance=request.user)
        profile_form = ProfileEditForm(
            data=request.POST or None, instance=request.user.profile, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            # return HttpResponseRedirect(reverse('edit_profile'))
            return HttpResponseRedirect(reverse('profile_info', args=[request.user.profile.id]))
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'home/edit_profile.html', context)

def image_edit(request, id):
    image = get_object_or_404(Image, id=id)
    if image.author != request.user:
        raise Http404()
    if request.method == 'POST':
        form = ImageEditForm(request.POST or None, request.FILES or None, instance=image)
        if form.is_valid():
            form.save()
            # return HttpResponseRedirect(image.get_absolute_url())
            return HttpResponseRedirect(reverse('dashboard', args=[request.user.profile.id]))
    else:
        form = ImageEditForm(instance=image)
    context = {
        'form': form,
        'image': image,
    }
    return render(request, 'home/image_edit.html', context)

def image_delete(request, id):
    image = get_object_or_404(Image, id=id)
    if request.user != image.author:
        raise Http404()
    image.delete()
    # return redirect('index')
    return HttpResponseRedirect(reverse('dashboard', args=[request.user.profile.id]))
