from app import app
from app.models import Category, Product , User
import hashlib


def load_categories():

    return Category.query.all()


def load_products(cate_id=None , kw =None):

    query = Product.query
    if cate_id:
        query = query.filter(Product.category_id.__eq__(cate_id))
    if kw:
        # Tương đương với mênh đề WHERE LIKE
        # nó sẽ lấy kw bên của index.py
        query = query.filter(Product.name.contains(kw))
    return  query.all()
#Lấy id product
def get_product_by_id(product_id):
    # lấy product_id dưới CSDL
    return Product.query.get(product_id)

#Cho người dùng nhập mật khẩu
#Strip() cắt khoảng trắng 2 đầu
def auth_user(username , password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).digest()) #nữa dùng .hexdigest()
    return User.query.filter(User.username.__eq__(username.strip()), User.password.__eq__(password)).first()
def get_user_id(user_id):
    return User.query.get(user_id)