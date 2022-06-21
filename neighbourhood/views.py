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
    posts=Post.objects.filter(neighbourhood = user.profile.neighbourhood)
    return render(request, 'index.html',{"posts":posts,"neighbourhoods":user.profile.neighbourhood,"user":user,"hoods":hoods,"business":business})

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

    user=request.user
    if request.method =='POST':
        if Profile.objects.filter(user_id=user).exists():
            form = UpdateProfile(request.POST,request.FILES,instance=Profile.objects.get(user_id = user))
        else:
            form=UpdateProfile(request.POST,request.FILES)
        if form.is_valid():
          profile=form.save(commit=False)
          profile.user=user
          profile.save()
        return redirect('profile',user.id)
    else:

        if Profile.objects.filter(user_id = user).exists():
           form=UpdateProfile(instance =Profile.objects.get(user_id=user))
        else:
            form=UpdateProfile()

    return render(request,'editprofile.html',{"form":form})

def neighbourhoods(request):
    user=request.user
    hoods=NeighbourHood.objects.all()

    if request.method == 'POST':
        form = UpdateNeighbourhood(request.POST,request.FILES,instance=Profile.objects.get(user_id = user))
        if form.is_valid:
            profile = form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('index')
    else:
        form = UpdateNeighbourhood()

    return render (request,'neighbourhood.html',{"user":user,"hoods":hoods,"form":form})
    
@login_required()
def create_neighbourhood(request):

    if request.method=='post':
        form=NeighbourhoodForm(request.POST,request.files)
        if form.is_valid:
            neighbour=form.save(commit=False)
            neighbour.user=user
            neighbour.save()
            return redirect(index)

        else:
            form=NeighbourhoodForm()
        return render(request,'neighform.html',{"form":form})

@login_required()
def neighbourhood_details(request,neighbour_id):
    user=request.user
    details=NeighbourHood.objects.get(id=neighbour_id)
    user.profile.neighbourhood = details
    business=Business.get_business_by_estate(neighbour_id)
    posts=Post.get_post_by_estate(neighbour_id)

    if request.method == 'POST':
        form = BusinessForm(request.POST, request.FILES)
        if form.is_valid:
            name = form.data.get('name')
            email = form.data.get('email')
            description = form.data.get('description')
            post = form.save(commit=False)
            post.user = user
            post.save()
            return redirect('index')

    else:
        form = BusinessForm()

    return render(request,'singlehood.html',{"details":details, "business":business, "posts":posts, 'form':form})

def create_business(request):
    '''
    View function to post a message
    '''
    user = request.user

    if request.method == 'POST':
        form = BusinessForm(request.POST, request.FILES)
        if form.is_valid:
            post = form.save(commit=False)
            post.user = user
            post.neighbourhood = user.profile.neighbourhood
            post.save()
            return redirect(index)

    else:
        form = BusinessForm()
    return render(request, 'new-business.html', {"form":form})

@login_required()
def business_details(request, business_id):
    '''
    View function to view details of a hood
    '''
    details = Business.get_specific_business(business_id)

    return render(request, 'business-details.html',{"details":details})

@login_required()
def new_post(request):
    user = request.user
    posts =Profile.objects.get(user = request.user.id)
    if request.method =='POST':
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = user
            project.user_profile = posts
            project.save()
        return redirect('index')

    else:
        form = PostForm()

    return render(request,'post.html',{"form":form})


def search_results(request):
    if 'business' in request.GET and request.GET['business']:
        search_term = request.GET.get('business')
        searched_business = Business.search_business(search_term)
        message = f"{search_term}"
        return render(request, 'results.html', {"message": message, "search_term":search_term, "results": searched_business})
    else:
        message = 'Try Again'
        return render(request, 'results.html', {"message": message})
    