from app import db
from app.models import Category, Product, User, Receipt, ReceiptDetails
import hashlib
from flask_login import  current_user
# Import khi thông kê báo cáo
from sqlalchemy import  func

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


# phan trang

#Lấy id product
def get_product_by_id(product_id):
    # lấy product_id dưới CSDL
    return Product.query.get(product_id)

#Cho người dùng nhập mật khẩu
#Strip() cắt khoảng trắng 2 đầu
def auth_user(username , password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest()) #nữa dùng .hexdigest()
    return User.query.filter(User.username.__eq__(username.strip()), User.password.__eq__(password)).first()
def get_user_id(user_id):
    return User.query.get(user_id)
# Truyền các name đúng tên bên templates bến register.html
def register(name,username,password,avatar):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())  #nữa dô làm nhớ truyền hexdigest()
    # Chữ màu trắng là thuộc tính trong User của bên models
    u = User(name=name, username=username.strip() , password = password , avatar = avatar)
    db.session.add(u)
    db.session.commit()
def save_receipt(cart):
    if cart:
        # user va receipt là của bref trên product
     r = Receipt(user = current_user )
     db.session.add(r)
     for c in cart.values():
        d= ReceiptDetails(quantity=c['quantity'], price = c['price'], receipt=r , product_id= c['id'])
        db.session.add(d)
     db.session.commit()

#Thong ke bao cáo
def count_product_by_cate():
    # isouter =True sẽ in ra tất cả các category -> dù có sản phẩm có hay không
    return db.session.query(Category.id , Category.name,func.count(Product.id))\
        .join(Product, Product.category_id.__eq__(Category.id) ,isouter=True)\
        .group_by(Category.id).all()

def stats_revenue(kw=None, from_date=None, to_date=None):
    query = db.session.query(Product.id, Product.name, func.sum(ReceiptDetails.quantity*ReceiptDetails.price))\
                      .join(ReceiptDetails, ReceiptDetails.product_id.__eq__(Product.id))\
                      .join(Receipt, ReceiptDetails.receipt_id.__eq__(Receipt.id))

    if kw:
        query = query.filter(Product.name.contains(kw))

    if from_date:
        query = query.filter(Receipt.created_date.__ge__(from_date))

    if to_date:
        query = query.filter(Receipt.created_date.__le__(to_date))

    return query.group_by(Product.id).order_by(-Product.id).all()

if __name__ == "__main__" :
    from app import app
    with app.app_context():
        print(count_product_by_cate())

















