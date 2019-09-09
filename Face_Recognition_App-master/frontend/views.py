from __future__ import unicode_literals
from .serializers import UserSerializer, ImageSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.decorators import action
from rest_framework import mixins
from rest_framework import status
from rest_framework.parsers import JSONParser
from django.db.models import Q
from django.views.generic.edit import CreateView
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, reverse, redirect, get_object_or_404
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from django.contrib.auth import login as django_login, logout as django_logout
from .serializers import LoginSerializer
from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from .forms import UserForm
from .models import User, Image
from rest_framework import viewsets
from .serializers import UserSerializer
import os
from .serializers import UserSerializer , checkimageserializer

# class userview(ListModelMixin , GenericAPIView):
#     print('hey')
#     serializer_class = UserSerializer
#     queryset = Users.objects.all()
#     print(queryset)
#     #return Response({"User": User})

#     def perform_create(self, serializer):
#         Users = get_object_or_404(Users, id=self.request.data.get('Users_id'))
#         return serializer.save(Users=Users)

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


def register(request):
    # print(os.system(pwd))
    return render(request, 'register.html', {'msg': 'Fill the Form', 'status': 'warning'})


def upload(request):
    if request.method == 'POST':
        try:
            name = request.POST['name']
            email = request.POST['email']
            user = User(name=name, email=email)
            user.save()
            for file in request.FILES.getlist('user_img'):
                img = Image(user=user, user_img=file)
                img.save()
                user.img.add(img)
            user.save()
            return render(request, 'register.html', {'msg': 'Data Uploaded Successfully', 'status': 'success'})
        except Exception as e:
            return render(request, 'register.html', {'msg': "User already exists! Try again with different name.", 'status': 'danger'})
    return HttpResponseRedirect('/')


# from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework.filters import OrderingFilter, SearchFilter
# from django_filters import FilterSet
# from django_filters import rest_framework as filters


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        django_login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "message": "User Successfully Logged in."}, status=200)


class LogoutView(APIView):
    authentication_classes = (TokenAuthentication)

    def post(self, request):
        django_logout(request)
        return Response(status=204)




class PollListView(generics.GenericAPIView,
                   mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'id'
    authentication_classes = [TokenAuthentication,
                              SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, id=None):
        if id:
            return self.retrieve(request, id)
        else:
            return self.list(request)

    def post(self, request):
        return self.create(request)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def put(self, request, id=None):
        return self.update(request, id)

    def perform_update(self, serializer):
        print(self.request.user)
        serializer.save(created_by=self.request.user)

    def delete(self, request, id=None):
        return self.destroy(request, id)


class userviewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class imgviewset(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = checkimageserializer

from rest_framework import serializers
from rest_framework import views
from rest_framework.views import APIView
from django.shortcuts import render
from django.http import Http404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
import json
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser , FileUploadParser
import os
import cv2,pickle
import face_recognition as fr
import numpy as np
from PIL import Image
from .models import Check_Image
import requests
import base64


@api_view(["POST"])
def img_check(request):
    print('you entered')
    print(request)
    print(request.FILES)
    img_r = request.FILES['img']
    #print(image)
    print(img_r)


    img_obj = Check_Image(image=img_r)
    img_obj.save()

    Cimage = open("sample.jpeg" , "wb")
    Cimage.write(requests.get("http://127.0.0.1:8000/media/Check_Image/"+str(img_r)).content)
    Cimage.close()
    
    
    # q = os.getcwd()
    # o = os.mkdir(q + "/" + image)
    #image = request.data
    #calling this function
    # logo = Image(image)
    # logo.save('logo.jpeg')
    # logo.show()
    # dataset = os.getcwd()+"/"+str(image)

    #create_known_face_encodings()

    #loading those binary files
    font=cv2.FONT_HERSHEY_SIMPLEX
    with open("encodings.txt",'rb') as file_data:
        known_face_encodings=pickle.load(file_data)
        
    with open("name.txt",'rb') as file_data:
        known_names=pickle.load(file_data)
        #print(known_face_encodings)
    #taking image path as input from user
    #img_path=input("Enter the image path you want to match:-")

    #reading image
    print('hey')
    #print(img_obj.image)
    #imagee = Image.open(img_obj.image)
    #print(image)
    #imagee.show()
    img=cv2.imread("sample.jpeg")
    #print(img)
    process_this_img = True
    #converting BGR image to RGB image
    rgb_img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    if process_this_img:
        #gettting face locations
        face_locations=fr.face_locations(rgb_img)
        #getting face encodings
        current_face_encoding=fr.face_encodings(rgb_img,face_locations)
        print(current_face_encoding)
        print(len(current_face_encoding))
        print(len(known_face_encodings))
        print("==================")
        #print(known_face_encodings)
        for face_encoding in current_face_encoding:
            #compariong face with known faces
            #print("d")
            print(face_encoding)

            name="unknown"
            matches=fr.compare_faces(known_face_encodings,face_encoding)
            print("jdiv")
            print(matches)
        #get a euclidean distance for each comparison face. The distance tells you how similar the faces are.
            face_distances = fr.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_names[best_match_index]
                print(name)
                accurate=(1.0-min(face_distances))*100
                print(accurate)
    # process_this_frame = not process_this_img
    # for (top, right, bottom, left) in face_locations:
    #     #creating a rectangle around face in frame				
    #     cv2.rectangle(img,(left,top),(right,bottom),(0,255,0),1)
    #     #putting image name on the top of rectangle 
    #     cv2.putText(img, name, (left , top), font, 1.0, (255, 225, 0), 4)
    #     cv2.putText(img,str(accurate), (10,50), font, 1.0, (255, 225, 0), 4)		
    #showing our image 
    #cv2.namedWindow('Live',cv2.WINDOW_NORMAL)
    #cv2.resizeWindow('Live', 600,600)
    #cv2.imshow("Live",img)
    #cv2.waitKey(0)		
    #cv2.destroyAllWindows()

    return Response(name)




def create_known_face_encodings():
    known_face_encodings_list=[]
    known_names=[]
    font=cv2.FONT_HERSHEY_SIMPLEX
    #creating image's directory
    try:
        #getting current working directory
            cwd=os.getcwd()
        #creating a directory to store dataset images
            os.mkdir(cwd+"/media/user_images")
    except:
            print()

    dataset_dir=os.getcwd()+"/media/user_images/"
    #print(dataset_dir)
    image_path=os.listdir(dataset_dir)
    for i in image_path:
        #accessing each image
            image=dataset_dir+i
            print(image)
            known_face= fr.load_image_file(image)
            #getting encodings of faces
            known_face_encoding=fr.face_encodings(known_face)
            if len(known_face_encoding) > 0:
                known_face_encoding=fr.face_encodings(known_face)[0]
            else:
                print("fail")
        #getting image names
            image_name=i.split("_")[0]
            known_face_encodings_list.append(known_face_encoding)
            known_names.append(image_name)
        #print(known_face_encodings_list)
        #dumping encodings in encodings.txt in binary mode
    with open("encodings.txt",'wb') as file_data:
            pickle.dump(known_face_encodings_list,file_data)
        #dumping image names in name.txt in binary mode
    with open("name.txt",'wb') as file_data:
            pickle.dump(known_names,file_data)








    #try:
     #   print('entry')
      #  print(request)
       # value =  json.loads(request.body)       
        #print('entry')
        #print (value)       
        #su = sum(value)
        #print(su)
        #return Response("Sum is :"+str(su))
    #except:
     #   return Response(status.HTTP_400_BAD_REQUEST)
    

    #def get(self, request):
        # Validate the incoming input (provided through query parameters)
        #serializer = IncredibleInputSerializer(data=request.query_params)
        #serializer.is_valid(raise_exception=True)

        # Get the model input
        #data = serializer.validated_data
        #model_input = data["i"]

        # Perform the complex calculations
        #complex_result = model_input + "xyz"

        # Return it in your custom format

class FileUploadView(views.APIView):
    parser_classes = [FileUploadParser]

    def post(self, request, filename ,format=None):
        try:
            file_obj = request.data['file']
            print(file_obj)
            if(file_obj):
                return Response(status=200)
        except:
            return Response(status=400)
        return Response(status=204)
