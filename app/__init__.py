from flask import Flask
# thêm này để có kết nối với CSDL
from flask_sqlalchemy import SQLAlchemy
#Sau khi đã thêm bên dao
from flask_login import LoginManager

app = Flask(__name__)  # Sau khi đã refactor từ bên index
# Để thao tác trên create trên admin được
app.secret_key ="@$@#$@#$@#$!@#@Q#"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/saleapp?charset=utf8mb4'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
# Đây là tên biến để truy vấn dữ liệu -> và tạo file models
login = LoginManager(app=app)
db = SQLAlchemy(app=app)