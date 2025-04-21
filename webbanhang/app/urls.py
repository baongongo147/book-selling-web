# Được sử dụng để định nghĩa các hàm xử lý yêu cầu từ phía người dùng và trả về các phản hồi tương ứng. 
# Cụ thể, file này chứa các hàm view, là các hàm Python có nhiệm vụ xử lý logic của ứng dụng web, từ việc truy xuất dữ liệu từ cơ sở dữ liệu, xử lý dữ liệu, đến việc render các template và trả về các phản hồi HTTP.
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),                              
    path('cart/', views.cart, name='cart'),                         # trỏ đến views được gọi là cart
    path('checkout/', views.checkout, name='checkout'),             # trỏ đến views được gọi là checkout
    path('update_item/', views.updateItem, name='update_item'),     # trỏ đến views được gọi là update_item
    path('login/', views.loginpage, name='login'),                  # trỏ đến views được gọi là login
    path('logout/', views.logoutpage, name='logout'),               # trỏ đến views được gọi là logout
    path('signup/', views.signup, name='signup'),                   # trỏ đến views được gọi là signup
    path('gioithieu/', views.gioithieu, name='gioithieu'),          # trỏ đến views được gọi là gioithieu
]
