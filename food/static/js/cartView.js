if(document.readyState == 'loading'){
	document.addEventListener('DOMContentLoaded',ready)
}else{
	ready()
}

function ready(){

var removeCartItemButtons = document.getElementsByClassName('far fa-times-circle')

console.log(removeCartItemButtons)

for(var i = 0; i < removeCartItemButtons.length; i++){
		var button = removeCartItemButtons[i]
		button.addEventListener('click', function(event) {
			var buttonClicked = event.target
			buttonClicked.parentElement.parentElement.remove()
			updateCartTotal()
		})
} 

}


function updateCartTotal(){
	var cartItemContainer  = document.getElementsByClassName('cart_items')[0]
	var cartRows = cartItemContainer.getElementsByClassName('listitems')
	var total = 0
	for(var i = 0; i < cartRows.length; i++){
		var cartRow  = cartRows[i]
		var priceElement  = cartRow.getElementsByClassName('cart-price')[0]
		var price = parseInt(priceElement.innerText.replace('₹',''))
		total  = total + price
	}	
	document.getElementsByClassName('price-total')[0].innerText = 'subtotal ' + '₹' + total
};