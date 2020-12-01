from django.urls import path

from taskapp.views import user_api, user_crud,loginuser,verifyOtp,resetpwd

urlpatterns = [

  path('new/', view=user_api,name='user_api'),
  path('test/<int:id>/', view=user_crud,name='user_crud'),
  path('login/', view=loginuser,name='loginuser'),
  path('verify/', view=verifyOtp,name='verifyOtp'),
  path('reset/', view=resetpwd,name='resetpwd'),


]