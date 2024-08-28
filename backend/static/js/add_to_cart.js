$(document).ready(function() {
    // Get the product ID from the script tag
    const productId = JSON.parse($('#product-id').text());

    // Handle the Add to Cart button click
    $('.add-to-cart').click(function() {
        // Get selected options
        const size = $('#size').val();
        const color = $('#color').val();
        const quantity = $('#quantity').val();

        // Prepare data to send to the server
        const cartData = {
            product_id: productId,
            size: size,
            color: color,
            quantity: quantity
        };

        // Send data to the server
        $.ajax({
            type: 'POST',
            url: '/add_to_cart', // Your Flask route for adding to cart
            contentType: 'application/json',
            data: JSON.stringify(cartData),
            success: function(response) {
                alert('Product added to cart!');
                // Optionally update the UI or redirect
            },
            error: function(xhr) {
                alert('Failed to add product to cart.');
            }
        });
    });
});
