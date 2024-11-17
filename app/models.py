from token import COLON

from sqlalchemy import Column, Integer, String, Text, Float, Boolean, ForeignKey , Enum,  DateTime


from app import db, app
# Phải them dong nay để cấu hình mối quan hệ Association
from sqlalchemy.orm import relationship, backref
from enum import Enum as UserEnum
#pip install flask-login
from flask_login import UserMixin
from datetime import datetime

# Clas BaseModel được tạo ra để gom nhóm những thuộc tính chung lại

class BaseModel(db.Model):
    __abstract__ = True  # Để cho nó không tạo bảng
    id = Column(Integer, primary_key=True, autoincrement=True)


# VÀ Cho nó kế thừa BaseModel
class Category(BaseModel):
    # Chỉ định tên bản tự tạo
    __tablename__ = 'category'
    # Khóa chính và tự động tăng
    # nullable -> không được phép trùng , không được phép trống
    name = Column(String(50), nullable=False, unique=True)
    # bên nào cho đi khóa chính để làm khóa ngoại bên kia sẽ có dòng này
    # danh sách sản phẩm thuộc vào Cate này
    # backref để truyền vào procduct -> để product có thể lay dc category của nó
    # Luôn bật là true để tránh lấy những product không cần giảm tốc độ truy vấn
    products = relationship('Product', backref='category', lazy=True)

    # ToString để nó hiện tên lên trên chứ không in ra đối tượng ví dụ như Điện thoại thay vì <Category 1>
    def __str__(self):
        return self.name


class Product(BaseModel):
    # __tablename__ ='product'
    name = Column(String(50), nullable=False)
    description = Column(Text)  # Khi dùng Text thì nho import và sqlalchemy
    price = Column(Float, default=0)  # Float cũng vay
    image = Column(String(100))
    active = Column(Boolean, default=True)
    # Cấu hình khóa ngoại tạo ra sản phẩm phải có danh mục nullable = False
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    receipt_details = relationship('ReceiptDetails', backref='product', lazy=True)
    #Lấy tag ra không lấy sản phẩm ra
    tags =relationship('Tag',secondary='pro_tag',lazy='subquery',backref=backref('products ', lazy=True))
    def __str__(self):
        return self.name

    #
    #
    #
    # Sau khi gõ code nhớ Run chổ if __name__ này để nó tạo bảng dưới CSDL

class UserRole(UserEnum):
    USER = 1
    ADMIN =2
class User(BaseModel ,UserMixin):
    name = Column(String(50) , nullable=False)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    active = Column(Boolean)   #Nữa cacsi nullable = True hoặc không ghi để bên def register không cần truyền vào
    avatar = Column(String(100),nullable=False )
    user_role = Column(Enum(UserRole) , default=UserRole.USER) #mặc định là user -> đề tài nữa tạo phải gán giáo viên hoặc nhân viên .
    receipts = relationship('Receipt', backref='user', lazy=True)
    def __str__(self):
        return self.name
class Receipt(BaseModel):
    create_date = Column(DateTime, default=datetime.now())
    user_id = Column(Integer , ForeignKey(User.id) , nullable=False)
    details = relationship('ReceiptDetails' , backref='receipt', lazy=True)
class ReceiptDetails(BaseModel):
    quantity = Column(Integer , default=0)
    price = Column(Float , default=0)
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False )
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False)

class Tag(BaseModel):
    name = Column(String(50), nullable=False,unique=True)
    def __str__(self):
        self.name
#2N2
#Nếu hàm này viết sau thì foreignKey khong cần ('product.id') -> product là tên bản còn nếu viết sau thì viết như bên dưới tên class.id
prod_tag = db.Table('pro_tag',
                    Column('product_id' ,Integer ,ForeignKey(Product.id),primary_key=True),
                    Column('tag_id',Integer,ForeignKey(Tag.id),primary_key=True))
if __name__ == "__main__":
    with app.app_context():
        # # Gio them cac doi tượng vào bảng
        # cate1 = Category(name="Điện thoại")
        # cate2 = Category(name="Máy tính bảng")
        # cate3 = Category(name="Phụ Kiện")
        # db.session.add_all([cate1, cate2, cate3])

        # Cái cate PC mình thêm dưới CSDL
        #
        # p1 = Product(name='IPHONE 13 PROMAX' , description='RAM 156GB' , price='13000000' , image ='https://24hstore.vn/images/products/2024/09/10/large/iphone-16-1.jpg', category_id=1)
        # p2 = Product(name='IPHONE 12 PROMAX', description='RAM 256GB', price='12000000',image='https://24hstore.vn/images/products/2024/08/22/large/iphone-15-pro-hinh-1.jpg', category_id=1)
        # p3 = Product(name='IPHONE 11 PROMAX', description='RAM 64GB', price='10000000',image='https://24hstore.vn/images/products/2024/09/10/large/iphone-16-pro-01.jpg',category_id=1)
        # p4 = Product(name='IPHONE 15 PROMAX', description='RAM 1TB', price='20000000',image='https://24hstore.vn/images/products/2023/09/27/large/iphone%2015%20Plus%20black_1695790477_1.jpg', category_id=1)
        # p5 = Product(name='IPAD 15 PROMAX', description='RAM 1TB', price='25000000',image='https://24hstore.vn/images/products/2024/10/18/large/ipad-mini-7-wifi-cellular-512gb-tim.jpg',category_id=2)
        #
        # # # # Dùng để truy vấn (cập nhật dữ liệu xuống CSDL) -> Cập nhật sản phẩm vào bảng
        # db.session.add_all([p1,p2,p3,p4,p5])
        # db.session.commit()



       # Bâm mật khẩu ra
       # import hashlib
       # password = str(hashlib.md5('123456'.encode('utf-8')).hexdigest()) #.hexdigest() thay vì dùng digest()
       # u = User(name='theanh',username='admin', password=password , active=True, user_role=UserRole.ADMIN, avatar='')
       # db.session.add(u)
       # db.session.commit()


        # Dùng để tạo bảng trong CSDL -> hoặc tạo 1 cột cho bảng
        # Và nếu có thể các cột trong CSDL thì chạy lại nó đóng mấy cái kia lại
        db.create_all()