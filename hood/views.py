from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
# Create your views here.

def home(request):
    title = 'Home'
    if request.user.is_authenticated():
        profile = Bio.get_bio_by_user(request.user)
        
        if request.method == 'POST':
            form = StatusForm(request.POST)
            if form.is_valid():
                status = form.save(commit=False)
                status.user = request.user
                status.hood = profile.user_hood
                status.save()
        else:
            form = StatusForm()

        return render(request, 'index.html',{
            'title':title,
            'profile':profile,
            'form': form,
            
        })
    else:
        return redirect('/accounts/login/')

def profile(request, username):
    profile = User.objects.get(username=username)
    try:
        profile_details = Profile.get_by_id(profile.id)
    except:
        profile_details = Profile.filter_by_id(profile.id)
    images = Image.get_profile_images(profile.id)
    title = f'@{profile.username} Hood-watch'

    return render(request, 'profile/profile.html', {'title':title, 'profile':profile, 'profile_details':profile_details})

    title = f'@{username}'

    statuses = Status.status_by_user(username)
    profile = Bio.get_bio_by_user(username)

    if request.method == 'POST':
        form = StatusForm(request.POST)
        if form.is_valid():
            status = form.save(commit=False)
            status.user = request.user
            status.hood = profile.user_hood
            status.save()
    else:
        form = StatusForm()

    return render(request, 'profile/profile.html',{
        'title':title,
        'form':form,
        'profile':profile,
        'statuses':statuses,
    })

@login_required(login_url='/accounts/login')
def profile_bio(request, username):
    title = 'Bio'
    profile = Bio.get_bio_by_user(username)

    if request.method == 'POST':
        user_form = EditUser(instance=request.user, data=request.POST)
        bio_form = BioForm(instance = request.user.bio, data=request.POST)
        hood_form = HoodForm(request.POST)
        if bio_form.is_valid() and user_form.is_valid() and hood_form.is_valid():
            user_form.save()
            hood_form.save()
            bio_form.save()

        
    
    else:
        bio_form = BioForm(instance=request.user.bio)
        user_form = EditUser(instance=request.user)
        hood_form = HoodForm()


    return render(request, 'profile/bio.html', {
        'title':title,
        'form':bio_form,
        'hood_form':hood_form,
        'user_form':user_form,
        'profile':profile,
    })

@login_required(login_url='/accounts/login')
def profile_business(request, username):
    title = 'Business'

    businesses = Business.get_business_by_user(username)
    profile = Bio.get_bio_by_user(username)

    # if request.method == 'POST':
    #     business_form = BusinessForm(request.POST)
    #     if business_form.is_valid():
    #         business = business_form.save(commit=False)
    #         business.user = request.user
    #         business.save()
    #         business=BusinessForm()
    # else:
    business_form = BusinessForm()

    return render(request, 'profile/business.html', {
        'title':title,
        'form': business_form,
        'businesses':businesses,
        'profile':profile,
    })

def new_business(request):
    business_name = request.POST.get('business_name')
    business_email = request.POST.get('business_email')
    business_hood = request.POST.get('business_hood')

    business = Business(business_name=business_name, business_email=business_email, business_hood_id=business_hood, user = request.user)
    business.save()
    data = {'success': 'Business has been successfully added'}
    return JsonResponse(data)