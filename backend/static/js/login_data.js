$(document).ready(function() {
    $('#login-form').on('submit', function(event) {
        event.preventDefault(); // Prevent the default form submission

        var formData = {
            'email': $('#email').val(),
            'password': $('#password').val()
        };

        $.ajax({
            url: '/login',
            type: 'POST',
            data: formData,
            success: function(response) {
                // Save response data to localStorage
                if (response.error){
                    return alert(response.error)
                }
                localStorage.setItem('user_id', response.user_id);
                localStorage.setItem('user_name', response.user_name);
                localStorage.setItem('user_email', response.user_email);

                // Redirect to the main page after successful login
                window.location.href = '/'; // Replace with your actual main page route
            },
            error: function() {
                alert('Login failed. Please check your credentials and try again.');
            }
        });
    });
});