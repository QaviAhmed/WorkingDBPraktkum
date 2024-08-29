$(document).ready(function () {
    const user_exists = localStorage.getItem("user_id");
    $('.add-to-cart').click(function () {
        if(user_exists){
            var productId = $('.product-info').data('id');
            var quantityValue = $('#quantity').val();
            
            if (quantityValue === "") {
                alert("Please enter a quantity."); // Check if quantity input is empty
                return;
            }
        
            // Retrieve cart from localStorage or create a new one
            var cart = JSON.parse(localStorage.getItem('cart')) || [];
            
            // Add the product ID to the cart if it doesn't already exist
            if (!cart.includes(productId)) {
                cart.push({ "productId": productId, "quantity": quantityValue });
                localStorage.setItem('cart', JSON.stringify(cart));
                alert('Product added to cart!');
            } else {
                alert('Product already in cart!');
            }
            document.getElementById("cart_items_total").innerHTML = JSON.parse(localStorage.getItem('cart')).length
        }else{
            alert("please login first")
        }
    });

});
$(document).ready(function () {
    // Retrieve the cart from localStorage
    var cart = JSON.parse(localStorage.getItem('cart')) || [];
    var totalPrice = 0;
    const userId = localStorage.getItem('user_id');
    var product_list = [];

    // Check if the cart is empty
    if (cart.length === 0) {
        $('#cart-items').html('<p>Your cart is empty.</p>');
    } else {
        cart.forEach(function (item, index) {
            // Parse the product information
            var product_data = item;  // Assuming the cart now stores objects with productId and quantity

            $.ajax({
                url: '/api/product/' + product_data.productId,
                method: 'GET',
                success: function (product) {
                    var itemPrice = product.price * product_data.quantity; // Calculate price based on quantity
                    totalPrice += itemPrice;

                    // Append the product to the cart display
                    $('#cart-items').append(`
                        <div class="cart-item">
                            <div class="item-number">${index + 1}.</div>
                            <div class="item-image">
                                <img src="/backend/static/pics/product_images/${product.image}" alt="Product Image">
                            </div>
                            <div class="item-details">
                                <p>Quantity: ${product_data.quantity}</p>
                                <p>Details:<br>${product.name}<br>${product.description}</p>
                            </div>
                            <div class="item-price">${itemPrice.toFixed(2)} €</div>
                        </div>
                    `);

                    // Update total price
                    $('#cart-total').text(totalPrice.toFixed(2) + '€');

                    // Add the product with quantity to the product list
                    product_list.push({
                        product_id: product_data.productId,
                        quantity: product_data.quantity,
                        price: product.price // Include price for later use
                    });
                },
                error: function(xhr, status, error) {
                    console.error("Error fetching product details:", error);
                }
            });
        });
    }

    // Handle the "Buy now!" button click
    $('.checkout-button').on('click', function() {
        if (!userId || product_list.length === 0) {
            alert("No user logged in or cart is empty.");
            return;
        }

        const orderData = {
            order_id: Date.now(),
            user_id: userId,
            products: product_list
        };

        $.ajax({
            url: '/create_order', // Your Flask route for creating an order
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(orderData),
            success: function(response) {
                alert('Order placed successfully!');
                // Optionally clear the cart after successful order
                localStorage.removeItem('cart');
                window.location.href = '/order-success'; // Redirect to a success page
            },
            error: function(xhr, status, error) {
                console.error("Error placing order:", error);
                alert('Failed to place the order.');
            }
        });
    });
});
