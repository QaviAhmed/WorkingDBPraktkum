$(document).ready(function() {
    $('#upload-button').click(function() {
        // Convert the image to a Blob
        var blob = $('#profile-pic').imageBlob().blob();

        // Create a FormData object to prepare for the upload
        var formData = new FormData();
        formData.append('file', blob, 'profile-pic.jpg');

        // Perform the AJAX request to upload the blob
        $.ajax('/upload', {
            type: 'POST',
            data: formData,
            processData: false, // Prevent jQuery from automatically transforming the data into a query string
            contentType: false, // Prevent jQuery from setting the content type
            success: function(response) {
                alert('Upload successful: ' + response.message);
            },
            error: function(jqXHR, textStatus, errorThrown) {
                alert('Upload failed: ' + textStatus + ' ' + errorThrown);
            }
        });
    });
});

$(document).ready(function() {
    $('#updateProductForm').on('submit', function(e) {
        e.preventDefault(); // Prevent the default form submission

        // Get the form data
        var formData = new FormData(this);

        $.ajax({
            url: "{{ url_for('products_page.update_product') }}", // The URL to make the request
            type: 'PUT', // The HTTP method to use
            data: formData,
            contentType: false, // Important: set contentType to false for FormData
            processData: false,  // Important: do not process the data as URL-encoded params
            success: function(response) {
                alert('Product updated successfully');
                // Optionally, redirect or update the page content
                window.location.href = "{{ url_for('main_page') }}";
            },
            error: function(xhr, status, error) {
                alert('Error updating product: ' + xhr.responseText);
            }
        });
    });
});
