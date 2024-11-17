
from tempfile import template

from flask import render_template, request, redirect , session ,jsonify
# sau khi đã refactor qua bên init
from app import app, dao, login ,utils
# import admin vào
from flask_login import login_user, logout_user, current_user , login_required
import cloudinary.uploader
from app.decorators import annonymous_user

# Phải có cái này thì những gì viết bên bên admin.py mới chạy
from app import admin



# __name__ nó sẽ tự hieu là tên của package python
@app.route('/')  # @saleapp nếu như saleapp = Flask(...)
# @login_required #Nay gan vao dau thi dang nhap moi duoc thay trang -> Này do flask viet san nua co the custom lai chi cho admin thay trang admin da dang nhap
def index():
    # return  'hello the anh'
    cate_id = request.args.get('category_id')
    # Sau khi viết cate_id thì qua bên dao.py truyền vào load_product
    # Sau khi thêm bên kia sẽ thêm kw vao để truyền

    # Lấy name ='keyword' bên name='keyword' của index.html
    kw = request.args.get('keyword')
    products = dao.load_products(cate_id=cate_id, kw=kw)
    return render_template('index.html', products=products)  # nó sẽ tự động tìm trong templates


# categories red là biến dùng ngoài templates -> nghĩa là trên index nó dùng ,  còn màu trắng là biến = dao.load_categories

# Thêm phương thức ở đây để có thể truyền lên trên thanh của web
# Phải có dấu / đầu  và product_id phải parse về số nguyên .
@app.route('/product/<int:product_id>')
def detail(product_id):
    # Khi đã cài bên dao thì qua đùng cài cái này để truyền lên templates
    p = dao.get_product_by_id(product_id)
    return render_template('detail.html', product=p)


# Sau khi đã sửa bên index.html của admin thêm dòng này vào
@app.route('/login-admin', methods=['post'])
def admin_login():
    username = request.form['username']
    password = request.form['password']
    user = dao.auth_user(username=username, password=password)

    if user:
         login_user(user=user)
    # Chuyển trang -> cụ thể là chuyển về trang chủ

    return redirect('/admin')


# KHi qua trang khác sẽ hiện toàn bộ thanh navbar chứ không cần phải truyền  vào render_template categories
# chỉ cần có phương thức dưới thì những thằng nào có render_template đều sẽ có navbar hiên full categories
@app.context_processor
def common_attr():
    categories = dao.load_categories()
    return {
        'categories': categories,
        'cart' : utils.cart_stats(session.get(app.config['CART_KEY']))
    }


@login.user_loader
def load_user(user_id):
    return dao.get_user_id(user_id)


# Sau khi thêm qua bên index.html của admin thêm method="post"


# Đăng ký

# get trong cái này dùng để lấy đường dãn tới trang đăng ký còn post để lấy thông tin kiểm tra người dùng
@app.route('/register', methods=['get', 'post'])
def register():
    err_msg = ''
    if request.method.__eq__('POST'):
        password = request.form['password']
        confirm = request.form['confirm']
        if password.__eq__(confirm):
            # upload

            # 2 dòng này debug
            # import pdb
            # pdb.set_trace()
            avatar = ''
            if request.files:
                res = cloudinary.uploader.upload(request.files['avatar'])
                avatar = res['secure_url']
            # save_user
            try:
                dao.register(name=request.form['name'],
                             username=request.form['username'],
                             password=password, avatar=avatar)
                return redirect('/login')
            except:
                err_msg = " Hệ thống đang có lỗi! Vui lòng quay lại sau!"
        # pip install cloudinary
        else:
            err_msg = 'Mật khẩu không khớp'

    # nếu không phải post thì nó đi tới trang này ->
    return render_template('register.html', err_msg=err_msg)


@app.route('/login', methods=['get','post'])
# @annonymous_user #Nghĩa là annonymous này nó bọc def_login_my_user hay login_my_user = f vơí annonymous_user(f)
def login_my_user():
    # POST ở mấy thằng truyền vào  phải viết hoa
    if request.method.__eq__('POST'):
        # Lấy username của người dùng so sanh với của request ( hãy người dùng nhập)
        username = request.form['username']
        password = request.form['password']
        # Truyền hàm chứng thực người dùng vào
        user = dao.auth_user(username=username, password=password)
        if user:
            login_user(user=user)
            n = request.args.get('next')
            #  về trang chủ
            return redirect(n if n else'/') #Và xóa action /login

    # get vào trang
    return render_template('login.html')
# Xoá trạng thái đặng nhập khỏi session
@app.route('/logout')
def logout_my_user():
    logout_user()
    # đằng xuất là về login
    return redirect('login')
@app.route('/cart')
def cart():
    # session['cart'] = {
    #     "1":{
    #         "id":"1",
    #         "name":"Iphone15",
    #         "price":100000000,
    #         "quantity":1
    # #quantity số lượng trong giỏ
    #
    # },
    #     "2":{
    #         "id":"2",
    #         "name":"Iphone14",
    #         "price":200000000,
    #         "quantity":4
    # #quantity số lượng trong giỏ
    #
    # }
    # }
    return render_template('cart.html')
@app.route('/api/cart', methods=['post'])
def add_to_cart():
    data = request.json
    id = str(data['id'])
    name = data['name']
    price = data['price']
    key = app.config['CART_KEY'] #cart
    # Nếu có cart rồi thì dùng không thì tạo rỗng
    cart = session[key] if key in session else {}
    #Nếu có sp tăng lên
    if id in cart:
        cart[id]['quantity'] +=1
    #Nếu không có thì lấy sp ra
    else:
        name = data['name']
        price = data['price']
        cart[id]= {
            "id": id,
            "name": name,
            "price": price,
            "quantity": 1
        }
    session[key] = cart

    return jsonify(utils.cart_stats(cart=cart))
@app.route('/api/cart/<product_id>',methods=['put'])
def update_cart(product_id):
    key  = app.config['CART_KEY']
    cart = session.get(key)
    if cart and product_id in cart :
        cart[product_id]['quantity']= int(request.json['quantity'])

    session[key]= cart

    return jsonify(utils.cart_stats(cart=cart))
@app.route('/api/cart/<product_id>',methods=['delete'])
def delete_cart(product_id):
    key  = app.config['CART_KEY']
    cart = session.get(key)
    if cart and product_id in cart :
       del cart[product_id]

    session[key]= cart
    return jsonify(utils.cart_stats(cart=cart))
@app.route('/api/pay')
# Dang nhap moi dc thanh toan
@login_required
def pay():
    key = app.config['CART_KEY']
    cart = session.get(key)
    try :
        dao.save_receipt(cart)
    except:
        pass
    else : #khong loi se chay
        del session[key]
    return  jsonify({'status':200})


if __name__ == '__main__':
    app.run(debug=True)  # port này thêm vào để làm port của /
