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
