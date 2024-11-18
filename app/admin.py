# import các models quản lý vào
import babel.localedata

# Thêm pip install flask_babelex -> để có thể sửa các thanh tiêu đề của admin -> như các thành filer -> được cộng điểm

from app.models import Category, Product ,Tag
from app import db, app ,dao
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from wtforms import TextAreaField
from wtforms.widgets import TextArea
from flask import request
# from flask_babel import Babel



# pip install flask-admin


# Tìm hiểu thêm để viết đa ngôn ngữ
# @babel.localeselector
# def load_lacale():
#     return 'vi'


# Phần này sửa lỗi lại
class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' ckeditor'
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()


class ProductView(ModelView):
    column_searchable_list = ['name', 'description']
    column_filters = ['name', 'price']
    can_view_details = True
    can_export = True

    def is_accessible(self):
        return current_user.is_authenticated

    # Ẩn cột
    column_exclude_list = ['image']
    column_labels = {
        'name': 'Tên sản phẩm',
        'description': 'Mô tả',
        'price': 'giá'
    }
    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']
    # Khi gan vay thi description se co trinh soan thao -> va qua ben detail.html them  |safe(đánh là mã an toàn)
    form_overrides = {
        'description': CKTextAreaField
    }


class CategoryView(ModelView):
    # truyền đúng tên products -> truyền như vậy mới Edit đc Category với hiện danh sách sản phẩm trong  1 Danh mục
    # column_list = ['id', 'name', 'products']
    can_view_details = True

    def is_accessible(self):
        return current_user.is_authenticated


# Ở chổ này có thể viet phuong thuc is_accesible -> Cho phep xem khi da dang nhap vao mot lop base


# Thống kê báo cáo
class StatsView(BaseView):
    @expose('/')
    def index(self):
        stats = dao.stats_revenue(kw=request.args.get('kw'),
                                  from_date=request.args.get('from_date'),
                                  to_date=request.args.get('to_date'))
        return self.render('admin/stats.html', stats=stats)

    def is_accessible(self):
        return current_user.is_authenticated
#Khi đã import AdminIndexView thì ta viết lớp này để có thể đổ dữ liệu ra dùng
class MyAdminView(AdminIndexView):
    @expose('/')
    def index(self):
        stats = dao.count_product_by_cate()

        return  self.render('admin/index.html', stats=stats)

admin = Admin(app=app, name='Quản trị bán hàng', template_mode='bootstrap4',index_view=MyAdminView())
# Thêm các models muốn quản trị
admin.add_view(CategoryView(Category, db.session, name='Danh mục'))
admin.add_view(ProductView(Product, db.session, name='Sản phẩm'))
admin.add_view(ModelView(Tag, db.session, name='Nhãn sản phẩm'))
admin.add_view(StatsView(name='Thống kê'))

# Làm xong nhớ import vào bên index.py
