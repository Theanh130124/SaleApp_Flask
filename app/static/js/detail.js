function spinner(status="block") {
    let s = document.getElementsByClassName("spinner")
    for (let i = 0; i < s.length; i++)
        s[i].style.display = status
}

function loadComments(productId) {
    spinner()
    fetch(`/api/products/${productId}/comments`).then(res => res.json()).then(data => {
        spinner("none")
        let h = ""
        data.forEach(c => {
            h += `
            <li class="list-group-item">
              <div class="row">
                  <div class="col-md-1 col-sm-4">
                      <img src="${c.user.avatar}"
                        class="rounded-circle img-fluid" width="100%" />
                  </div>
                  <div class="col-md-11 col-sm-8">
                      <p>${c.content}</p>
                      <small>Bình luận <span class="text-info">${moment(c.created_date).locale('vi').fromNow()}</span> bởi <span class="text-info">${c.user.name}</span></small>
                  </div>
              </div>
            </li>
            `
        })

        let d = document.getElementById("comments")
        d.innerHTML = h
    })


}

function addComment(productId) {
    spinner()
     fetch(`/api/products/${productId}/comments`, {
        method: "post",
        body: JSON.stringify({
            "content": document.getElementById('comment-content').value
        }),
        headers: {
            "Content-Type": "application/json"
        }
    }).then(res => res.json()).then(data => {
        spinner("none")
        if (data.status === 204) {
            let c = data.comment
            let h = `
            <li class="list-group-item">
              <div class="row">
                  <div class="col-md-1 col-sm-4">
                      <img src="${c.user.avatar}"
                        class="rounded-circle img-fluid" width="100%" />
                  </div>
                  <div class="col-md-11 col-sm-8">
                      <p>${c.content}</p>
                      <small>Bình luận <span class="text-info">${moment(c.created_date).locale('vi').fromNow()}</span> bởi <span class="text-info">${c.user.name}</span></small>
                  </div>
              </div>
            </li>
            `
            let d = document.getElementById("comments")
            d.innerHTML = h + d.innerHTML
        } else
            alert("Hệ thống đang có lỗi!")

    }) // js promise
}