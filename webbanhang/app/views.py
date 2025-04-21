from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import *
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.

def loginpage(request):                                                     # Xử lí yêu cầu trang đăng nhập người dùng
    if request.user.is_authenticated:                                       # kiểm tra xem người dùng đã đăng nhập chưa  bằng cách sử dụng request.user.is_authenticated
        return redirect('home')                                             # Nếu đã đăng nhập sẽ trỏ đến trang home
    # Nếu không có người dùng nào đăng nhập, hàm tiếp tục kiểm tra xem yêu cầu được gửi lên từ trình duyệt có phải là phương thức POST không. 
    if request.method == "POST":                                            # Nếu là POST, nghĩa là người dùng đã gửi thông tin đăng nhập.
        username = request.POST.get('username')                             # Lấy thông tin username từ dữ liệu POST được gửi lên từ trình duyệt
        password = request.POST.get('password')                             # Lấy thông tin passwword từ dữ liệu POST được gửi lên từ trình duyệt
        user = authenticate(request, username=username, password=password)  # Sử dụng hàm authenticate để kiểm tra xem có người dùng nào tồn tại trong hệ thống với username và password được cung cấp hay không
        if user is not None:                                                # Nếu người dùng tồn tại
            login(request, user)                                            # Sử dụng login để đăng nhập    
            return redirect('home')                                         # Chuyển đến trang home
        else: messages.info(request, 'user or password not correct!')       # Nếu người dùng không tồn tại: Thêm một tin nhắn thông báo lỗi vào request bằng 'messages.info',  sau đó trả về trang đăng nhập với thông báo lỗi
    context={}                                                              # Nếu không có yêu cầu POST hoặc thông tin đăng nhập không hợp lệ, trả về trang đăng nhập với một context trống
    return render(request, 'app/login.html', context)                       # Trả về trang đăng nhập (login.html) cùng với context

def signup(request):                                                        # Xử lí yêu cầu trang đăng kí người dùng
    form = CreateUserForm()                                                 # khởi tạo form: dùng để nhập thông tin đăng kí người dùng
    if request.method == "POST":                                            # Nếu yêu cầu được gửi từ trình duyệt là phương thức POST, nghĩa là người dùng đã gửi thông tin đăng ký
        form = CreateUserForm(request.POST)                                 # Tạo form mới từ dữ liệu POST được gửi lên từ trình duyệt
        if form.is_valid():                                                 # Kiểm tra xem dữ liệu nhập vào form có hợp lệ không bằng cách sử dụng form.is_valid()
            form.save()                                                     # Nếu hợp lệ (tất cả các trường đã được điền đúng và không có lỗi) thì lưu thông tin đăng ký vào cơ sở dữ liệu bằng cách sử dụng form.save()
    context={'form': form}                                                  # Tạo một context chứa form để hiển thị trên trang đăng ký
    return render(request, 'app/signup.html', context)                      # Trả về trang đăng ký (signup.html) cùng với context, cho phép người dùng nhập thông tin đăng ký mới nếu cần

def home(request):                                                          # Xử lí yêu cầu trang home từ người dùng
    if request.user.is_authenticated:                                       # Kiểm tra xem người dùng đã đăng nhập hay chưa bằng cách sử dụng request.user.is_authenticated
        # Nếu người dùng đã đăng nhập:
        customer = request.user.customer                                    # Lấy thông tin khách hàng của người dùng từ cơ sở dữ liệu
        order, created = Order.objects.get_or_create(customer=customer, complete=False) # Lấy thông tin đơn hàng của người dùng từ cơ sở dữ liệu. Nếu không có đơn hàng nào tồn tại cho khách hàng này, tạo một đơn hàng mới
        items = order.orderitem_set.all()                                   # Lấy danh sách các mặt hàng trong đơn hàng của người dùng
        cartItems = order.get_cart_items                                    # Lấy số lượng các mặt hàng trong giỏ hàng, tính tổng số lượng các mặt hàng trong đơn hàng và lưu vào biến cartItems
    else:                                                                   # Nếu người dùng chưa đăng nhập, khởi tạo các giá trị mặc định cho các biến liên quan đến giỏ hàng
        items = []                                                          
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_items']
    products = Product.objects.all()                                        # Lấy danh sách tất cả các sản phẩm từ cơ sở dữ liệu
    context={'products': products, 'cartItems': cartItems}                  # Tạo một context chứa danh sách sản phẩm và số lượng mặt hàng trong giỏ hàng
    return render(request, 'app/home.html', context)                        # Trả về trang home (home.html) cùng với context

def cart(request):                                                          # Xử lí yêu cầu trong trang giỏ hàng của người dùng
    if request.user.is_authenticated:                                       # Kiểm tra xem người dùng đã đăng nhập hay chưa bằng cách sử dụng request.user.is_authenticated
        # Nếu người dùng đã đăng nhập: 
        customer = request.user.customer                                    # Lấy thông tin khách hàng của người dùng từ cơ sở dữ liệu
        order, created = Order.objects.get_or_create(customer=customer, complete=False) # Lấy thông tin đơn hàng của người dùng từ cơ sở dữ liệu. Nếu không có đơn hàng nào tồn tại cho khách hàng này, tạo một đơn hàng mới
        items = order.orderitem_set.all()                                   # Lấy danh sách các mặt hàng trong đơn hàng của người dùng
        cartItems = order.get_cart_items                                    # Lấy số lượng các mặt hàng trong giỏ hàng, tính tổng số lượng các mặt hàng trong đơn hàng và lưu vào biến cartItems
    else:                                                                   # Nếu người dùng chưa đăng nhập, khởi tạo các giá trị mặc định cho các biến liên quan đến giỏ hàng
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_items']
    context={'items': items, 'order': order, 'cartItems': cartItems}        # Tạo một context chứa danh sách các mặt hàng trong giỏ hàng, thông tin đơn hàng và số lượng mặt hàng trong giỏ hàng
    return render(request, 'app/cart.html', context)                        # Trả về trang cart (cart.html) cùng với context

def checkout(request):                                                      # Xử lí và hiển thị trang checkout
    if request.user.is_authenticated:                                       # Kiểm tra xem người dùng đã đăng nhập hay chưa bằng cách sử dụng request.user.is_authenticated
        # Nếu người dùng đã đăng nhập:
        customer = request.user.customer                                    # Lấy thông tin khách hàng của người dùng từ cơ sở dữ liệu
        order, created = Order.objects.get_or_create(customer=customer, complete=False) # Lấy thông tin đơn hàng của người dùng từ cơ sở dữ liệu. Nếu không có đơn hàng nào tồn tại cho khách hàng này, tạo một đơn hàng mới
        items = order.orderitem_set.all()                                   # Lấy danh sách các mặt hàng trong đơn hàng của người dùng
        cartItems = order.get_cart_items                                    # Lấy số lượng các mặt hàng trong giỏ hàng, tính tổng số lượng các mặt hàng trong đơn hàng và lưu vào biến cartItems 
    else:                                                                   # Nếu người dùng chưa đăng nhập, khởi tạo các giá trị mặc định cho các biến liên quan đến giỏ hàng
        items = []                                          
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_items']
    context={'items': items, 'order': order, 'cartItems': cartItems}        # Tạo một context chứa danh sách các mặt hàng trong giỏ hàng, thông tin đơn hàng và số lượng mặt hàng trong giỏ hàng
    return render(request, 'app/checkout.html', context)                    # Trả về trang checkout (checkout.html) cùng với context

def updateItem(request):                                                    # Cập nhật số lượng của một mặt hàng trong giỏ hàng khi người dùng thực hiện thao tác thêm hoặc xóa mặt hàng
    data = json.loads(request.body)                                         # Load và gán dữ liệu được gửi từ client đến server thông qua request.body được giải mã từ JSON thành một đối tượng Python sử dụng json.loads(request.body)
    productId = data['productId']                                           # Lấy ID của product từ dữ liệu được giải mã và gán vào biến productId
    action = data['action']                                                 # Lấy action từ dữ liệu được giải mã và gán vào biến action
    customer = request.user.customer                                        # Xác định khách hàng hiện tại bằng cách sử dụng request.user.customer và gán vào customer
    product = Product.objects.get(id = productId)                           # Lấy sản phẩm (Product) tương ứng với productId đã nhận được
    order, created = Order.objects.get_or_create(customer=customer, complete=False)     # Lấy thông tin đơn hàng của người dùng từ cơ sở dữ liệu. Nếu không có đơn hàng nào tồn tại cho khách hàng này, tạo một đơn hàng mới
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)  # Lấy thông tin về mục đơn hàng (OrderItem) cho sản phẩm trong đơn hàng. Nếu mục đơn hàng chưa tồn tại, hàm sẽ tạo mới một mục đơn hàng cho sản phẩm trong đơn hàng
    # Dựa vào hành động (action) được gửi từ client, cập nhật số lượng của mục đơn hàng:
    if action == 'add':             # Nếu hành động là 'add':
        orderItem.quantity += 1     # Tăng số lượng lên 1
    elif action == 'remove':        # Nếu hành động là 'remove':
        orderItem.quantity -= 1     # Giảm số lượng đi 1
    orderItem.save()                # Lưu mục đơn hàng sau khi đã cập nhật số lượng bằng hàm save()
    if orderItem.quantity <= 0:     # Nếu số lượng của mục đơn hàng nhỏ hơn hoặc bằng 0, xóa mục đó khỏi đơn hàng
        orderItem.delete()
    return JsonResponse('added', safe=False)                                # Trả về một JsonResponse thông báo rằng thao tác đã được thực hiện thành công

def gioithieu(request):                                                     # Xử lý yêu cầu trang giới thiệu từ người dùng
    context={}
    return render(request, 'app/gioithieu.html', context)                   # Trả về trang giới thiệu (gioithieu.html) cùng với context

def logoutpage(request):                                                    # Xử lý yêu cầu đăng xuất từ người dùng
    logout(request)                                                         # Sử dụng logout(request) để đăng xuất người dùng
    return redirect('home')                                                 # Chuyển hướng người dùng đến trang home (redirect('home'))      (hàm redirect được dùng để chuyển hướng người dùng đến một URL cụ thể)