from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm  

# Create your models here.

# Change forms register django:
class CreateUserForm(UserCreationForm):         # Định nghĩa một form trong Django dựa trên UserCreationForm của Django: được sử dụng để tạo người dùng mới
    class Meta:                                 # Được sử dụng để cung cấp thông tin về metadata của lớp form
        model = User                            # Xác định model mà form sẽ được tạo ra dựa trên
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']     # Xác định các trường mà form sẽ hiển thị. Các trường này bao gồm tên người dùng, email, tên, họ và hai trường mật khẩu

class Customer(models.Model):                   # Thông tin của khách hàng được lưu trong cơ sở dữ liệu
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=False)    # Định nghĩa 1 trường user, là một khóa ngoại trỏ đến model User trong django.contrib.auth.models
    # OneToOneField chỉ ra rằng mỗi khách hàng chỉ có một người dùng tương ứng, và ngược lại
    # Tham số on_delete=models.SET_NULL chỉ định hành động khi người dùng tương ứng bị xóa
    # null=True cho phép giá trị của trường user có thể là NULL
    # blank=False đảm bảo rằng trường này không thể bỏ trống trong các biểu mẫu
    name = models.CharField(max_length=200, null=True)  # Định nghĩa một trường name dạng ký tự với độ dài tối đa là 200 ký tự. Trường này được sử dụng để lưu tên của khách hàng
    email = models.CharField(max_length=200, null=True) # Định nghĩa một trường email dạng ký tự với độ dài tối đa là 200 ký tự. Trường này được sử dụng để lưu địa chỉ email của khách hàng
    
    def __str__(self):      # Định nghĩa phương thức __str__ để hiển thị một đối tượng Customer dưới dạng chuỗi
        return self.name    # Trả về tên của khách hàng

class Product(models.Model):        # Thông tin của một sản phẩm trong cơ sở dữ liệu
    name = models.CharField(max_length=200, null=True)                      # Định nghĩa một trường name dạng ký tự với độ dài tối đa là 200 ký tự. Trường này được sử dụng để lưu tên của sản phẩm.
    price = models.FloatField()                                             # Định nghĩa một trường price dạng số thực. Trường này được sử dụng để lưu giá của sản phẩm
    digital = models.BooleanField(default=False, null=True, blank=False)    # Định nghĩa một trường digital dạng boolean. Trường này chỉ ra liệu sản phẩm có phải là sản phẩm kỹ thuật số hay không (Thực tế ở đây muốn kiểm tra xem sách có ebook hay không)
    # default=False đặt giá trị mặc định của trường là False
    # null=True cho phép giá trị của trường có thể là NULL
    # blank=False đảm bảo rằng trường này không thể bỏ trống trong các biểu mẫu
    image = models.ImageField(null=True, blank=True)                        # Định nghĩa một trường image dạng ảnh. Trường này được sử dụng để lưu ảnh đại diện cho sản phẩm
    # null=True cho phép giá trị của trường có thể là NULL
    # blank=True cho phép trường này có thể bỏ trống trong các biểu mẫu

    def __str__(self):      # Định nghĩa phương thức __str__ để hiển thị một đối tượng Product dưới dạng chuỗi
        return self.name    # Trả về tên của sản phẩm
    
    @property               # Đây là một decorator của Python cho phép đánh dấu một phương thức để nó có thể được truy cập như một thuộc tính
    def ImageURL(self):     # Định nghĩa phương thức ImageURL để trả về đường dẫn của ảnh của sản phẩm
        try: 
            url = self.image.url
        except:
            url = ''
        return url

class Order(models.Model):      # Thông tin của một đơn hàng trong cơ sở dữ liệu
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank= True, null=True)   # Định nghĩa một trường customer dạng khóa ngoại (foreign key) đến model Customer. Trường này lưu thông tin về khách hàng của đơn hàng
    # on_delete=models.SET_NULL chỉ ra rằng nếu khách hàng liên quan bị xóa, trường customer của đơn hàng sẽ được đặt thành NULL
    # blank=True và null=True cho phép trường này có thể bỏ trống trong biểu mẫu
    date_order = models.DateTimeField(auto_now_add=True)                                        # Định nghĩa một trường date_order dạng thời gian và ngày, tự động được thiết lập khi đơn hàng được tạo (auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)                       # Định nghĩa một trường complete dạng boolean, chỉ ra liệu đơn hàng đã hoàn thành chưa
    # default=False đặt giá trị mặc định của trường là False
    # null=True cho phép giá trị của trường complete có thể là NULL
    # blank=False đảm bảo rằng trường này không thể bỏ trống trong các biểu mẫu
    transaction_id = models.CharField(max_length=200, null=True)                                # Định nghĩa một trường transaction_id dạng ký tự với độ dài tối đa là 200 ký tự. Trường này lưu mã giao dịch của đơn hàng
    
    def __str__(self):      # Định nghĩa phương thức __str__ để hiển thị một đối tượng Order dưới dạng chuỗi
        return str(self.id) # Trả về ID của đơn hàng

    @property   # Đây là một decorator của Python cho phép đánh dấu một phương thức để nó có thể được truy cập như một thuộc tính
    def get_cart_items(self):   # Hàm dùng để tính tổng số lượng các mục trong giỏ hàng của đơn hàng
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    
    @property   # Đây là một decorator của Python cho phép đánh dấu một phương thức để nó có thể được truy cập như một thuộc tính
    def get_cart_total(self):   # Hàm dùng để tính tổng giá trị của các mục trong giỏ hàng của đơn hàng
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

class OrderItem(models.Model):      # Dùng để lưu trữ thông tin về các mục trong đơn hàng
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank= True, null=True) # Định nghĩa một trường product dạng khóa ngoại đến model Product: Sản phẩm liên kết với mục đơn hàng, nếu sản phẩm được liên kết bị xóa, trường product sẽ được đặt thành NULL
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank= True, null=True)     # Định nghĩa một trường order dạng khóa ngoại đến model Order: Đơn hàng chứa mục đơn hàng, nếu đơn hàng liên quan bị xóa, trường order sẽ được đặt thành NULL.
    quantity = models.IntegerField(default=0, null=True, blank=True)                        # Định nghĩa một trường quantity dạng số nguyên: Số lượng của sản phẩm trong mục đơn hàng
    # default=0 đặt giá trị mặc định của trường là 0
    # null=True và blank=True cho phép trường này có thể bỏ trống
    date_added = models.DateTimeField(auto_now_add=True)                                    # Định nghĩa một trường date_added dạng thời gian và ngày, có thể tự động được thiết lập khi mục đơn hàng được tạo (auto_now_add=True)
    @property   # Đây là một decorator của Python cho phép đánh dấu một phương thức để nó có thể được truy cập như một thuộc tính
    def get_total(self):        # Hàm dùng để tính tổng giá trị của mục đơn hàng, bằng cách nhân giá của sản phẩm với số lượng của mục
        total = self.product.price * self.quantity
        return total            # trả về tổng giá trị
    
class ShippingAddress(models.Model):    # Lưu trữ thông tin về địa chỉ giao hàng của khách hàng 
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank= True, null=True)   # Định nghĩa một trường customer dạng khóa ngoại đến model Customer: khách hàng liên quan đến địa chỉ giao hàng
    # Nếu khách hàng được liên kết bị xóa, trường customer sẽ được đặt thành NULL
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank= True, null=True)         # Định nghĩa một trường order dạng khóa ngoại đến model Order: đơn hàng mà địa chỉ giao hàng thuộc về
    # Nếu đơn hàng liên quan bị xóa, trường order sẽ được đặt thành NULL
    address = models.CharField(max_length=200, null=True)                                       # Địa chỉ giao hàng của khách hàng, giới hạn tối đa 200 ký tự
    city = models.CharField(max_length=200, null=True)                                          # Thành phố của địa chỉ giao hàng, giới hạn tối đa 200 ký tự
    state = models.CharField(max_length=200, null=True)                                         # Bang hoặc tỉnh của địa chỉ giao hàng, giới hạn tối đa 200 ký tự
    mobile = models.CharField(max_length=10, null=True)                                         # Số điện thoại di động của khách hàng
    date_added = models.DateTimeField(auto_now_add=True)                                        # Thời gian và ngày, tự động được thiết lập khi bản ghi được tạo (auto_now_add=True)

    def __str__(self):                                                                          
        return self.address                                                                     # Trả về địa chỉ giao hàng