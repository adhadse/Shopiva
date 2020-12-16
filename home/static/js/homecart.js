window.addEventListener('load',function () {
    console.log('Loaded')
    var updateBtns = document.querySelectorAll('.update-cart')
    var wislistBtns = document.querySelectorAll('.update-wishlist')

    if (updateBtns) {
        for (let i = 0; i < updateBtns.length; i++) {
            updateBtns[i].addEventListener('click', function () {
                const productID = this.dataset.product
                const action = this.dataset.action
                console.log('productID:', productID, 'Action:', action)
                if (user === 'AnonymousUser') {
                    console.log('User is Anonymous')
                } else {
                    updateUserOrder(productID, action)
                }
            })
        }
    }
    if (wislistBtns) {
        for (let i = 0; i < wislistBtns.length; i++) {
            wislistBtns[i].addEventListener('click', function () {
                const productID = this.dataset.product
                const action = this.dataset.action
                console.log('productID:', productID, 'Action:', action)
                if (user === 'AnonymousUser') {
                    console.log('User is Anonymous')
                } else {
                    updateUserWishlist(productID, action)
                }
            })
        }
    }
})
function updateUserOrder(productID, action){
    console.log('user:',user,' is Authenticated, sending data')
    let url= '/api/update_item/'
    fetch(url,{
        method:'PUT',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'productID':productID, 'action':action})
    }).then((response)=>
        response.json()
    ).then(function (data){
            console.log('data:',data)
            updateOtherValues(data)
        })
}

function updateOtherValues(data){
    if (data['cartQuantity'] === 0){
        document.getElementById('cart').querySelectorAll('span').remove()
    }else if (document.getElementById('cart').querySelector('span') === null){
        document.getElementById('cart').innerHTML = 'Cart<span class="badge badge-danger" style="vertical-align: top;"><h7>' + data['cartQuantity'] + '</h7></span>'
    }
    else {
        document.getElementById('cart').querySelector('span').innerHTML = data['cartQuantity']
    }
}


function updateUserWishlist(productID,action){
    console.log('user:',user,' is Authenticated, sending data')
    let url= '/api/update_wishlist/'
    fetch(url,{
        method:'PUT',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'productID':productID, 'action':action})
    }).then((response)=>
        response.json()
    ).then(function (data){
            console.log('data:',data)
            updateNavbar(data)
        })
}

function updateNavbar(data){
    document.getElementById('wishlist').innerHTML = 'Wishlist<span class="badge badge-danger" style="vertical-align: top;"><h7>' + data['wishlistItemQuantity'] + '</h7></span>'
}
