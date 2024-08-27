$(document).ready(function() {
    $('.product-item').on('click', function() {
        var productId = $(this).data('product-id');
        window.location.href = '/product/' + productId;
    });
    window.alert("this is working")
});