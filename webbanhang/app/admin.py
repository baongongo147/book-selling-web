# Được sử dụng để đăng ký các model để hiển thị trong trang quản trị (admin site)
# Có thể tùy chỉnh cách các đối tượng của model được hiển thị và sửa đổi trong trang quản trị
from django.contrib import admin
from .models import *


# Register your models here.
# Đăng kí các model đã được định nghĩa trong file models.py của app để hiển thị lên trang admin
admin.site.register(Customer)           # Đăng ký model Customer để hiển thị trong trang quản trị
admin.site.register(Product)            # Đăng ký model Product để hiển thị trong trang quản trị
admin.site.register(Order)              # Đăng ký model Order để hiển thị trong trang quản trị
admin.site.register(OrderItem)          # Đăng ký model OrderItem để hiển thị trong trang quản trị
admin.site.register(ShippingAddress)    # Đăng ký model ShippingAddress để hiển thị trong trang quản trị