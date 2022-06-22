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

    if user.profile.neighbourhood :
        business=Business.objects.filter(neighbourhood=user.profile.neighbourhood)
        posts=Post.objects.filter(neighbourhood = user.profile.neighbourhood)
        details=NeighbourHood.objects.get(id=user.profile.neighbourhood.id)
    
        context = {
            "details":details,
            "business":business,
            "posts":posts,
            "neighbourhoods":user.profile.neighbourhood,
            "user":user,
            "hoods":hoods,
        }
    else:
        context = {
            "user":user,
            "hoods":hoods,
        }

    return render(request, 'index.html',context)

@login_required()
def profile(request, profile_id):
    '''
    Method that fetches a users profile page
    '''

    user=User.objects.get(pk=profile_id)
    title = User.objects.get(pk = profile_id).username
    profile = Profile.objects.filter(user = profile_id)
    return render(request,"profile.html",{"profile":profile,"title":title})

@login_required()
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

@login_required()
def updateProfile2(request, user_id):

    if request.method =='POST':
        if Profile.objects.filter(user_id=user_id).exists():
            form = UpdateProfile(request.POST,request.FILES,instance=Profile.objects.get(user_id = user_id))
        else:
            form=UpdateProfile(request.POST,request.FILES)
        if form.is_valid():
          profile=form.save(commit=False)
          profile.user.id=user_id
          profile.save()
        return redirect('allHoods')
    else:

        if Profile.objects.filter(user_id = user_id).exists():
           form=UpdateProfile(instance =Profile.objects.get(user_id=user_id))
        else:
            form=UpdateProfile()

    return render(request,'editprofile.html',{"form":form})

def neighbourhoods(request):
    user=request.user
    hoods=NeighbourHood.objects.all()
    users=User.objects.all()

    if request.method == 'POST':
        form = UpdateNeighbourhood(request.POST,request.FILES,instance=Profile.objects.get(user_id = user))
        if form.is_valid:
            profile = form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('index')
    else:
        form = UpdateNeighbourhood()

    return render (request,'neighbourhood.html',{"user":user,"hoods":hoods,"form":form, "users":users})
    
@login_required()
def create_neighbourhood(request):
    user = request.user
    if request.method=='POST':
        form=NeighbourhoodForm(request.POST,request.FILES)
        if form.is_valid:
            neighbourhood=form.save(commit=False)
            neighbourhood.user = user
            neighbourhood.save()
            return redirect('index')

    else:
        form=NeighbourhoodForm()
    return render(request,'newhood.html',{"form":form})

@login_required()
def neighbourhood_details(request,neighbour_id):
    user=request.user
    details=NeighbourHood.objects.get(id=neighbour_id)
    user.profile.neighbourhood = details
    business=Business.objects.filter(neighbourhood=user.profile.neighbourhood)
    posts=Post.get_post_by_neighbourhood(neighbour_id)

    if request.method == 'POST':
        form = BusinessForm(request.POST, request.FILES)
        if form.is_valid:
            name = form.data.get('name')
            email = form.data.get('email')
            description = form.data.get('description')
            business = form.save(commit=False)
            business.user = user
            business.neighbourhood = user.profile.neighbourhood
            business.save()
            return redirect('index')

    else:
        form = BusinessForm()

    return render(request,'singlehood.html',{"details":details, "business":business, "posts":posts, 'form':form})


@login_required()
def new_post(request):
    user = request.user
    posts =Profile.objects.get(user = request.user.id)
    if request.method =='POST':
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = user
            post.neighbourhood = user.profile.neighbourhood
            post.save()
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

def hood_occupants(request, hood_id):
    occupants = NeighbourHood.objects.get(id=hood_id)
    # occupants = Profile.objects.filter(neighbourhood=hood)
    return render(request, 'accounts.html', {'occupants': occupants})
    