
from tempfile import template

from flask import render_template, request, redirect , session ,jsonify
# sau khi đã refactor qua bên init
from app import app, dao, login ,utils ,controllers
# import admin vào
from flask_login import login_user, logout_user, current_user , login_required
import cloudinary.uploader
from app.decorators import annonymous_user

# Phải có cái này thì những gì viết bên bên admin.py mới chạy
from app import admin
# Không có dấu () là hàm chưa chạy vào trong moi chạy
app.add_url_rule("/" , 'index' , controllers.index)
# Tên sau controllers đặt đúng hàm bên controllers
#"login-admin"
# Đây là endpoint, một tên gọi duy nhất để tham chiếu đến quy tắc URL này.
# Flask sử dụng endpoint trong các thao tác như:
# Xây dựng URL: Dùng hàm url_for('login-admin') để tạo URL tương ứng.
# Phân biệt route: Endpoint cần là duy nhất trong ứng dụng.
# Nếu không chỉ định endpoint, Flask sẽ mặc định lấy tên hàm xử lý (ở đây là admin_login).
app.add_url_rule("/product/<int:product_id>", 'detail' ,controllers.detail)
app.add_url_rule('/login-admin', 'login-admin', controllers.admin_login, methods=['post'])
app.add_url_rule("/register",'register',controllers.register, methods=['get', 'post'])
app.add_url_rule("/login",'login',controllers.login_my_user ,methods=['get','post'])
app.add_url_rule('/logout','logout',controllers.logout_my_user)
app.add_url_rule("/cart","cart",controllers.cart)
app.add_url_rule("/api/cart","add_cart", controllers.add_to_cart, methods=['post'])
app.add_url_rule("/api/cart/<product_id>" ,"update_cart",controllers.update_cart , methods=['put'])
app.add_url_rule("/api/cart/<product_id>","delete_cart",controllers.delete_cart,methods=['delete'])
app.add_url_rule("/api/pay", controllers.pay)

#Chỉnh những hàm app.route
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
if __name__ == '__main__':
    app.run(debug=True)  # port này thêm vào để làm port của /
