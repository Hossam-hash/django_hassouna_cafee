from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.contrib import messages,auth
from .models import UserProfile
from products.models import Product
import re

# Create your views here.
def signin(request):
    if request.method== 'POST' and "btnsignin" in request.POST:
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            if "rememberme"  not in request.POST:
                request.session.set_expiry(0)
            auth.login(request,user)
            #messages.success(request,'you are ok')
        else:
            messages.error(request,'username or password is invalid')
        return  redirect('signin')
    else:
        return render(request,'accounts/signin.html')


def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect('index')


def signup(request):
    if request.method== 'POST' and "btnsignup" in request.POST:
        #variables for fields
        fname=None
        lname=None
        address=None
        address2=None
        city=None
        state=None
        zip=None
        email=None
        username=None
        password=None
        terms=None
        is_added=None
        if 'fname' in request.POST: fname=request.POST['fname']
        else:messages.error(request,'error in first name')
        if 'lname' in request.POST: lname=request.POST['lname']
        else:messages.error(request,'error in last name')
        if 'address' in request.POST: address=request.POST['address']
        else: messages.error(request, 'error in address1')
        if 'address2' in request.POST: address2=request.POST['address2']
        else:messages.error(request, 'error in address2')
        if 'city' in request.POST: city=request.POST['city']
        else: messages.error(request, 'error in city')
        if 'state' in request.POST: state=request.POST['state']
        else: messages.error(request, 'error in state name')
        if 'zip' in request.POST: zip=request.POST['zip']
        else:messages.error(request, 'error in zip code')
        if 'email' in request.POST: email=request.POST['email']
        else: messages.error(request, 'error in email')
        if 'username' in request.POST: username=request.POST['username']
        else: messages.error(request, 'error in username')
        if 'password' in request.POST: password=request.POST['password']
        else:messages.error(request, 'error in password')
        if 'terms' in request.POST: terms=request.POST['terms']
                #Check all values
        if fname and lname and address and address2 and city and state and zip and email and username and password :
            if terms == 'on':
                #check if the username is taken before
                if User.objects.filter(username=username).exists()==True:
                    messages.error(request,'This username is taken before')
                else:
                    if User.objects.filter(email=email).exists()==True:
                        messages.error(request, 'This email is taken before')
                    else:
                        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                        if re.match(pattern,email):
                            #add user
                            user=User.objects.create_user(first_name=fname,last_name=lname,email=email,username=username,password=password)
                            user.save()
                            #add profile
                            userprofile=UserProfile(user=user,address=address,address2=address2,city=city,state=state,zip_num=zip)
                            userprofile.save()
                            #clear fields
                            fname=''
                            lname=''
                            address=''
                            address2=''
                            city=''
                            state=''
                            zip=''
                            email=''
                            username=''
                            password=''
                            #success message
                            messages.success(request,'Your profile is created')
                            is_added=True
                        else:
                            messages.error(request,'invalid email')
            else:messages.error(request, 'you must agree to the terms')

        else:
            messages.error(request,'Check empty field ')
        return render(request,'accounts/signup.html',context={'fname':fname,'lname':lname,'address':address,
                                                              'address2':address2,'city':city,'zip':zip,'email':email
                                                               ,'username':username,'password':password,'state':state,'is_added':is_added})

    else:
        return render(request,'accounts/signup.html')
def profile(request):
    if request.method== 'POST'and 'btnsaveprofile' in request.POST :
        if request.user is not None and request.user.id != None:
            userprofile = UserProfile.objects.get(user=request.user)
            email = request.POST['email']
            fname=request.POST['fname']
            lname=request.POST['lname']
            address=request.POST['address']
            address2=request.POST['address2']
            city=request.POST['city']
            state=request.POST['state']
            zip=request.POST['zip']
            username = request.POST['username']
            password=request.POST['password']
            if fname and lname and address and address2 and city and state and zip and email and username and password:
                 request.user.first_name=fname
                 request.user.last_name=lname
                 userprofile.address=address
                 userprofile.address2=address2
                 userprofile.city=city
                 userprofile.state=state
                 userprofile.zip_num=zip
                 #request.user.email=email
                 #request.user.username=username
                 if not request.POST['password'].startswith('pbkdf2_sha256$6'):
                     request.user.set_password(request.POST['password'])
                 request.user.save()
                 userprofile.save()
                 auth.login(request,request.user)
            else:
                messages.error(request,'check your values and elements')
        return redirect('profile')
    else:
        #render basic informations
        context=None
        if not request.user.is_anonymous:
            if request.user is not None:
                userprofile = UserProfile.objects.get(user=request.user)
                context={
                    'fname':request.user.first_name,
                    'lname':request.user.last_name,
                    'address':userprofile.address,
                    'address2':userprofile.address2,
                    'city':userprofile.city,
                    'state':userprofile.state,
                    'zip':userprofile.zip_num,
                    'email':request.user.email,
                    'username':request.user.username,
                    'password':request.user.password,
                }
                return render(request,'accounts/profile.html',context)
        else:
            return redirect('profile')


def product_favourite(request,pro_id):
    if request.user.is_authenticated and not request.user.is_anonymous:
        pro_fav=Product.objects.get(pk=pro_id)
        if UserProfile.objects.filter(user=request.user,product_favourite=pro_fav).exists():
            messages.success(request,'this product is already added')
        else:
            userprofile=UserProfile.objects.get(user=request.user)
            userprofile.product_favourite.add(pro_fav)
            messages.success(request,'product has been favourite')
        return redirect('/products/'+str(pro_id))
    else:
        messages.error(request,'you must be login')
    return redirect('/products/'+str(pro_id))


def show_product_favourite(request):
    context=None
    if request.user.is_authenticated and not request.user.is_anonymous:
        userInfo=UserProfile.objects.get(user=request.user)
        pro=userInfo.product_favourite.all()
        context={
            'products':pro
        }
    return render(request,'products/products.html',context)
