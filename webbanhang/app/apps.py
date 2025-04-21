from django.apps import AppConfig

class AppConfig(AppConfig):     
    default_auto_field = 'django.db.models.BigAutoField'    # Đây là cấu hình mặc định cho trường khóa chính (primary key) của các model trong ứng dụng
    name = 'app'                                            # Xác định tên của ứng dụng
