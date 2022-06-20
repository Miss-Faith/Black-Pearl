from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from .forms import *
from django.template import loader

# Create your views here.
@login_required(login_url='/accounts/login/')
def index(request):
    current_user =request.user
    hoods=Neighbourhood.get_neighbourhoods
    est=Follow.objects.get(user = request.user)
    business=Business.get_business_by_neighbourhood(est.neighbourhood)
    post=Post.objects.all()
    return render(request, 'index.html',{"posts":post,"neighbourhoods":est,"user":current_user,"hoods":hoods,"business":business})

@login_required(login_url='/accounts/login/')
def profile(request,profile_id):
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

    return render(request,'update.html',{"form":form})

@login_required(login_url='/accounts/login/')
def follow(request,neighbour_id):
    current_user=request.user
    neighbourhood=Neighbourhood.objects.get(id=neighbour_id)
    following=Follow(user=current_user,neighbourhood=neighbourhood)
    check_if_exists=Follow.objects.filter(user=current_user).exists()
    if check_if_exists==True:
        Follow.objects.all().filter(user=current_user).delete()
        Follow.objects.update_or_create(user=current_user,neighbourhood=neighbourhood)
    else:
        following.save()
    return redirect(index)

@login_required(login_url='/accounts/login/')
def unfollow(request,id):
    current_user =request.user
    neighbourhood=Neighbourhood.object.get(id=id)
    following=Follow(user=current_user,neighbourhood=neighbourhood).delete()
    return redirect(index)


def neighbourhoods(request):
    current_user=request.user
    hoods=Neighbourhood.get_neighbourhoods
    return render (request,'neighbourhood.html',{"user":current_user,"hoods":hoods})
    
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
    if len(Follow.objects.all().filter(user=request.user))>0:
        details=Neighbourhood.get_specific_hood(neighbour_id)
        exists=Follow.objects.all().get(user=request.user)
    else:
        details=Neighbourhood.get_specific_hood(neighbour_id)
        exists=0
    return render(request,'neigh_details.html',{"exists":exists,"details":details})

def create_business(request):
    '''
    View function to post a message
    '''
    current_user = request.user
    est = Follow.objects.get(user = request.user.id)

    if request.method == 'POST':
        form = BusinessForm(request.POST, request.FILES)
        if form.is_valid:
            post = form.save(commit=False)
            post.user = current_user
            post.neighbourhood = est.neighbourhood
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
        form = PostMessageForm(request.POST,request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = current_user
            project.user_profile = posts
            project.save()
        return redirect('index')

    else:
        form = PostMessageForm()

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
    