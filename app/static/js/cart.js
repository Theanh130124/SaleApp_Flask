function addToCart(id , name , price){
//axios fetch
fetch('/api/cart',{
method : "post",
body :JSON.stringify({
    "id":id ,
    "name":name,
    "price":price
    }),
    headers: {
    "Content-Type" :"application/json"}
   }).then(res => res.json()).then(data => {
     console.info(data) //js promise
     let d = document.getElementsByClassName("cart-counter")
     for (let i = 0 ; i <d.length ; i++)
        d[i].innerText = data.total_quantity
        })
}

//Sau khi da cau hinh API tho qua ben index truyen func nay vao dat hang

function updateCart(productId , obj ) {
//Truyền literal
//trong feeth đúng với tên trong app_route
fetch(`api/cart/${productId}`,{
    method : "put",
    body :JSON.stringify({
        "quantity": obj.value
    }),
    headers: {
    "Content-Type" :"application/json"}
   }).then(res => res.json()).then(data => {
     console.info(data) //js promise
//     Muốn cập nhật những chổ khác chỉ cần gán class cart-counter
     let d = document.getElementsByClassName("cart-counter")
     for (let i = 0 ; i <d.length ; i++)
        d[i].innerText = data.total_quantity
     let d2 = document.getElementsByClassName("cart-amount")
     for (let i = 0 ; i <d2.length ; i++)
    //Thêm toLo...... để thay đổi tiền dấu phẩy không mất
        d2[i].innerText = data.total_amount.toLocaleString("en-US")
        })
}
function deleteCart(productId){
if ( confirm("Bạn có muốn xóa không ?")==true)
{
fetch(`api/cart/${productId}`,{
    method : "delete"
   }).then(res => res.json()).then(data => {
     console.info(data) //js promise
//     Muốn cập nhật những chổ khác chỉ cần gán class cart-counter
     let d = document.getElementsByClassName("cart-counter")
     for (let i = 0 ; i <d.length ; i++)
        d[i].innerText = data.total_quantity
     let d2 = document.getElementsByClassName("cart-amount")
     for (let i = 0 ; i <d2.length ; i++)
    //Thêm toLo...... để thay đổi tiền dấu phẩy không mất
        d2[i].innerText = data.total_amount.toLocaleString("en-US")
//        Để ản đi
     let c = document.getElementById(`cart${productId}`)
     c.style.display = "none"
        }).catch(err => console.info(err)) //Trả về lỗi

}
}
function pay(){
    if(confirm("Ban co chan chac thanh toan")==true)
        fetch("/api/pay").then(res => res.json()).then(data =>{
        //=== kiem tra ki
        if (data.status === 200 )
          location.reload() //F5
        else
         alert("Co loi xay ra")
         })

}
