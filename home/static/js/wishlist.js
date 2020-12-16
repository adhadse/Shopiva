window.addEventListener('load',function () {
    console.log('Loaded')
    const wislistBtns = document.querySelectorAll('.update-wishlist');
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
            if (data['deleted'] === true){
                itemDeleted(productID,data)
            } else {
                itemAddedToCart(productID, data)
            }
            if (data['wishlistItemQuantity']===0){
                document.getElementById('wishlist').innerHTML = 'Wishlist'
            }
        })
}

function itemDeleted(productID, data){
    //delete col update 'Wishlist''nav
    document.getElementById(productID).remove()
    document.getElementById('wishlist').innerHTML = 'Wishlist<span class="badge badge-danger" style="vertical-align: top;"><h7>' + data['wishlistItemQuantity'] + '</h7></span>'
}
function itemAddedToCart(productID, data){
    //delete col update 'Wishlist' & 'Cart'  nav
    document.getElementById(productID).remove()
    document.getElementById('wishlist').innerHTML = 'Wishlist<span class="badge badge-danger" style="vertical-align: top;"><h7>' + data['wishlistItemQuantity'] + '</h7></span>'
    document.getElementById('cart').innerHTML = 'Cart<span class="badge badge-danger" style="vertical-align: top;"><h7>' + data['cartItemQuantity'] + '</h7></span>'
}