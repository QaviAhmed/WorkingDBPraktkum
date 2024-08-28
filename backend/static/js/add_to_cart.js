$(document).ready(function () {
    $('.add-to-cart').click(function () {
        var productId = $('.product-info').data('id');
        
        // Retrieve cart from localStorage or create a new one
        var cart = JSON.parse(localStorage.getItem('cart')) || [];
        
        // Add the product ID to the cart if it doesn't already exist
        if (!cart.includes(productId)) {
            cart.push(productId);
            localStorage.setItem('cart', JSON.stringify(cart));
            alert('Product added to cart!');
        } else {
            alert('Product already in cart!');
        }
    });
});

$(document).ready(function () {
    // Retrieve the cart from localStorage
    var cart = JSON.parse(localStorage.getItem('cart')) || [];
    var totalPrice = 0;
    
    // Check if the cart is empty
    if (cart.length === 0) {
        $('#cart-items').html('<p>Your cart is empty.</p>');
    } else {
        cart.forEach(function (productId, index) {
            // Assuming you have an API endpoint to fetch product details by ID
            $.ajax({
                url: '/api/product/' + productId,
                method: 'GET',
                success: function (product) {
                    var itemPrice = product.price * 1; // Assuming quantity is 1 for simplicity
                    totalPrice += itemPrice;

                    $('#cart-items').append(`
                        <div class="cart-item">
                            <div class="item-number">${index + 1}.</div>
                            <div class="item-image">
                                <img src="/Users/qavi/Desktop/SS24/DB_Praktikum/WorkingDBPraktkum/backend/static/pics/product_images/"+${product['image']}>
                            </div>
                            <div class="item-details">
                                <p>Quantity: 1</p>
                                <p>Details:<br>${product['name']}<br>${product['description']}</p>
                            </div>
                            <div class="item-price">${itemPrice.toFixed(2)} €</div>
                        </div>
                    `);

                    // Update total price
                    $('#cart-total').text(totalPrice.toFixed(2) + '€');
                }
            });
        });
    }
});