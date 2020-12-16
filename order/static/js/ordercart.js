window.addEventListener('load',function () {
    console.log('Loaded')
    var updateBtns = document.querySelectorAll('.update-cart')

    if (updateBtns){
            for (let i = 0; i < updateBtns.length; i++) {
                updateBtns[i].addEventListener('click', function () {
                    const productID = this.dataset.product
                    const action = this.dataset.action
                    console.log('productID:', productID, 'Action:', action)
                    if (user === 'AnonymousUser'){
                        console.log('User is Anonymous')
                    }
                     else {
                         updateUserOrder(productID, action)
                    }
                })
            }
    }
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
            let list = data
            if (data['Deleted']=== true){
                deleteCard(productID,list)
            } else {
                updateCard(productID,list)
            }
            updateOtherValues(data)
        })

};

function deleteCard(productID,data){
    let card = document.getElementById(productID)
    card.remove()
}

function updateCard(productID, data){
    let card = document.getElementById(productID)
    let input = card.querySelector('div>div>div input')
    input.value = data['cartItemQuantity'];
    input.setAttribute('value', data['cartItemQuantity']);
    input.innerHTML= data['cartItemQuantity'];
    let orderItemTotal = card.querySelector('figcaption strong')
    orderItemTotal.innerHTML = '&#x20B9;'+data['cartItemTotal']
}

function updateOtherValues(data){

    let cartItemquantity = document.querySelector('article>dl>dt>span:first-child')
    cartItemquantity.innerHTML = data['cartQuantity'] + ' items';

    let subtotal = document.querySelector('article>dl>dd>strong:first-child')
    subtotal.innerHTML = '&#x20B9;'+data['cartTotal'];

    let Total = document.querySelector('section>div>div>main>article>dl>dd strong.text-dark')
    Total.innerHTML = '&#x20B9;'+data['cartTotal'];

    let overviewTotal = document.querySelector('aside>div>div>dl dd.h5')
    overviewTotal.innerHTML = '&#x20B9;'+data['cartTotal'];

    if (data['cartQuantity'] === 0){
        document.getElementById('cart').querySelector('span').remove()
        document.querySelector('aside>div>div>a button.btn-block').disabled = true;
        document.querySelector('aside>div>form>div>div>span button.btn').disabled = true;
    } else {
        document.getElementById('cart').querySelector('span h7').innerHTML = data['cartQuantity']
    }
}

