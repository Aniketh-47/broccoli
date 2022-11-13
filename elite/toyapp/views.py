from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from .models import Profile
from .models import UserDetails
from SavedModels.model import Model
import numpy as np
import torch
from torchvision import transforms
import cv2

# Create your views here.
def index(request):
    # return HttpResponse("this is main page")
    return render(request, 'index.html')

def msg(request):
    return render(request,'msg.html')

def register(request):
    if request.method=="POST":
        uname =request.POST.get('uname')
        email=request.POST.get('email')
        mobile=request.POST.get('mobile')
        check_profile=Profile.objects.filter(mobile=mobile).first()
        check_user = User.objects.filter(email=email).first()
        if check_profile or check_user :#
            context={'message' : 'User Already Exists ','class':'danger'}
            return render(request,'register.html',context)
        user=User(first_name=uname,email=email)
        user.save()
        #otp=str(random.randint(1000,9999))
        profile=Profile(user=user,mobile=mobile)#,otp=otp
        profile.save()
        #sendotp(mobile,otp)
        request.session['mobile']=mobile
        return redirect('/login')
    return render(request, 'register.html')


def login(request):
    try:
        if request.method == 'POST':
            mobile = request.POST.get('mobile')
            users = Profile.objects.filter(mobile=mobile).first()
            print(users)
            if mobile == users.mobile:
                return redirect('/user')

            else:
                context = {'message': 'User Not Found ', 'class': 'danger'}
                return render(request, 'login.html', context)

        return render(request, 'login.html')
    except TypeError:
        context = {'message': 'User Not Found ', 'class': 'danger'}
        return render(request, 'login.html', context)
    except AttributeError:
        context = {'message': 'User Not Found ', 'class': 'danger'}
        return render(request, 'login.html', context)

global image

def user(request):
    if request.method == 'POST':
        try:
            image = request.FILES['image']
        except Exception as e:
            print("Exception is ",e)
            return render(request,'user.html')    
        # print(type(image))
        # print("Yeah its working !!!")
        # print(image)
        us1 = UserDetails(image=image)
        us1.save()
       # print(predictor(image))
        path1 = "static/"+str(image)
        out12=predictor(image)
        
        
    
        return render(request,'user.html',{'out12':out12,'path1':path1})
           
    else:
        return render(request,'user.html')
    

def predictor(image):
        image_path = 'images/'+str(image)
        model_path = 'SavedModels/mymodel_mnist_0.99.pth.tar' #Write best trainig accuracy model here!   
        # print(image_path)  
        I = cv2.imread(image_path) 
        # print(I)
        if (I is None):
            return "in this image does not have right dimensions"
        
        else:
            resized_down = cv2.resize(I, (28, 28), interpolation= cv2.INTER_LINEAR)
        display_image = cv2.resize(I, (64, 64), interpolation= cv2.INTER_LINEAR)
        greyscale_image = cv2.cvtColor(resized_down, cv2.COLOR_BGR2GRAY)
        inverted_image = cv2.bitwise_not(greyscale_image)
    

        model = Model()
        model.load_state_dict(torch.load(model_path))  
        model.eval()
        transform_test = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
    ])
        classes = [i for i in range(10)]


    # (thresh, I1) = cv2.threshold(I, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        I1 = np.array(inverted_image)

        I1 = torch.tensor(I1)


    
        with torch.no_grad():
        
            I1 = torch.reshape(I1,(1, 1, 28, 28))

            output = model(I1.float()).detach()

            predict_y = np.argmax(output, axis=-1)
            answer = predict_y.numpy()[0]
        
            # print("The Number present in this image is : ",classes[answer])
            out =str(classes[answer])
            return out
            #return render(request,'user.html',{'out':out})
            
            # return "The Number present in this image is : " + str(classes[answer])
