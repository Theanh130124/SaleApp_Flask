#Các hàm này sẽ không liên quan đến CSDL -> Có thể là tính toàn tiền
#Nhằm phục vụ tiện ích cho web
def cart_stats(cart):
    total_amount , total_quantity = 0, 0
    if cart:
        # Lấy cả mảng cart -> có bao nhieu sản phẩm lấy hết
        for c in cart.values():
            total_quantity += c['quantity']
            total_amount += c['quantity']*c['price']
    return {
        "total_amount" : total_amount,
        "total_quantity" : total_quantity
    }