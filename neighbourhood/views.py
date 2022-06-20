from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from .forms import *
from django.template import loader

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            User.objects.create_user(username=username, email=email, password=password)
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required()
def index(request):
    user =request.user
    hoods=NeighbourHood.objects.all()
    business=Business.get_business_by_estate(user.profile.neighbourhood)
    post=Post.objects.all()
    return render(request, 'index.html',{"posts":post,"neighbourhoods":user.profile.neighbourhood,"user":user,"hoods":hoods,"business":business})

@login_required(login_url='/accounts/login/')
def profile(request, profile_id):
    '''
    Method that fetches a users profile page
    '''

    user=User.objects.get(pk=profile_id)
    title = User.objects.get(pk = profile_id).username
    profile = Profile.objects.filter(user = profile_id)
    return render(request,"profile.html",{"profile":profile,"title":title})

@login_required(login_url='/accounts/login/')
def updateProfile(request):

    current_user=request.user
    if request.method =='POST':
        if Profile.objects.filter(user_id=current_user).exists():
            form = UpdateProfile(request.POST,request.FILES,instance=Profile.objects.get(user_id = current_user))
        else:
            form=UpdateProfile(request.POST,request.FILES)
        if form.is_valid():
          profile=form.save(commit=False)
          profile.user=current_user
          profile.save()
        return redirect('profile',current_user.id)
    else:

        if Profile.objects.filter(user_id = current_user).exists():
           form=UpdateProfile(instance =Profile.objects.get(user_id=current_user))
        else:
            form=UpdateProfile()

    return render(request,'editprofile.html',{"form":form})

def neighbourhoods(request):
    user=request.user
    hoods=Neighbourhood.get_neighbourhoods
    return render (request,'neighbourhood.html',{"user":user,"hoods":hoods})
    
@login_required(login_url='/accounts/login')
def create_neighbourhood(request):

    if request.method=='post':
        form=NeighbourhoodForm(request.POST,request.files)
        if form.is_valid:
            neighbour=form.save(commit=False)
            neighbour.user=current_user
            neigghbour.save()
            return redirect(index)

        else:
            form=NeighbourhoodForm()
        return render(request,'neighform.html',{"form":form})

@login_required(login_url='/accounts/login')
def neighbourhood_details(request,neighbour_id):
    if len(Join_hood.objects.all().filter(user=request.user))>0:
        details=Neighbourhood.get_specific_hood(neighbour_id)
        exists=Join_hood.objects.all().get(user=request.user)
    else:
        details=Neighbourhood.get_specific_hood(neighbour_id)
        exists=0
    return render(request,'neigh_details.html',{"exists":exists,"details":details})

def create_business(request):
    '''
    View function to post a message
    '''
    current_user = request.user

    if request.method == 'POST':
        form = BusinessForm(request.POST, request.FILES)
        if form.is_valid:
            post = form.save(commit=False)
            post.user = current_user
            post.neighbourhood = user.profile.neighbourhood
            post.save()
            return redirect(index)

    else:
        form = BusinessForm()
    return render(request, 'new-business.html', {"form":form})

@login_required(login_url='/accounts/login')
def business_details(request, business_id):
    '''
    View function to view details of a hood
    '''
    details = Business.get_specific_business(business_id)

    return render(request, 'business-details.html',{"details":details})

@login_required(login_url='/accounts/login/')
def new_post(request):
    current_user = request.user
    posts =Profile.objects.get(user = request.user.id)
    if request.method =='POST':
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = current_user
            project.user_profile = posts
            project.save()
        return redirect('index')

    else:
        form = PostForm()

    return render(request,'new-project.html',{"form":form})


def search_results(request):
    if 'photos' in request.GET and request.GET['photos']:
        search_term = request.GET.get('photos')
        searched_photo = Images.search_by_title(search_term)
        photos = Images.objects.filter(name=searched_photo).all()
        message = f"{search_term}"
        return render(request, 'searched.html', {"message": message, "photos": searched_photo})
    else:
        message = 'Try Again'
        return render(request, 'searched.html', {"message": message})
    