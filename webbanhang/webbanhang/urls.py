"""
URL configuration for webbanhang project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# Load images
from django.conf.urls.static import static
from django.conf import settings

    
urlpatterns = [
    # Xác định cách điều hướng truy cập đến các trang trong ứng dụng Django, 
    # giúp Django biết các ánh xạ các yêu cầu từ trình duyệt đến các phần tử 
    # cụ thể của ứng dụng để phản hồi với dữ liệu hoặc giao diện tương ứng.
    path('admin/', admin.site.urls),     # trỏ đến trang quản trị của Django. Khi người dùng truy cập vào đường dẫn admin/ trên trình duyệt, Django sẽ chuyển hướng họ đến trang quản trị, nơi họ có thể quản lý các mô hình và dữ liệu của ứng dụng
    path('', include('app.urls')),       # được kích hoạt khi không có phần đường dẫn nào được cung cấp (đường dẫn gốc), được cấu hình để bao gồm các mẫu URL từ ứng dụng được gọi là app bằng cách sử dụng hàm include. Điều này có nghĩa là các mẫu URL được định nghĩa trong tệp urls.py của ứng dụng app sẽ được sử dụng khi đường dẫn gốc được truy cập.
]
# Load images: dùng để định cấu hình các URL pattern để phục vụ các tệp media
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)      # thêm một URL pattern cho phép Django phục vụ các tệp media từ thư mục MEDIA_ROOT khi được truy cập thông qua đường dẫn MEDIA_URL
