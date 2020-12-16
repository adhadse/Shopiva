window.addEventListener('load',function () {
        console.log('Loaded')
        var updateBtn = document.querySelector('.update-cart')

        updateBtn.addEventListener('click', function () {
            const productID = this.dataset.product
            const action = parseInt(document.getElementById('cart-quantity').getAttribute('value'),10);
            console.log('productID:', productID, 'Action:', action)
                    if (user === 'AnonymousUser'){
                        console.log('User is Anonymous')
                    }
                     else {
                         updateUserOrder(productID, action)
                    }
        })
    }
)

function updateUserOrder(productID, action){
    console.log('user:',user,' is Authenticated, sending data')
    let url= '/api/update_item/'
    fetch(url,{
        method:'PUT',
        headers:{
            'Content-Type':'application/json',
            'Accept': 'application/json',
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
function incrementValue()
{
    var value = parseInt(document.getElementById('cart-quantity').value, 10);
    value = isNaN(value) ? 0 : value;
    value++;
    document.getElementById('cart-quantity').value = value;
    document.getElementById('cart-quantity').setAttribute('value', value);
    document.getElementById('cart-quantity').innerHTML = value;
}
function decreamentValue()
{
    var value = parseInt(document.getElementById('cart-quantity').value, 10);
    value = isNaN(value) ? 0 : value;
    if (value !== 1){
        value--;
    }
    document.getElementById('cart-quantity').value = value;
    document.getElementById('cart-quantity').setAttribute('value', value);
    document.getElementById('cart-quantity').innerHTML = value;
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

