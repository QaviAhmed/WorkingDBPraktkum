$(document).ready(function() {
    const productId = JSON.parse($('#product-id').text());
    
    // Function to render feedback
    function renderFeedback(feedback) {
        const feedbackContainer = $('#feedback-container');
        feedbackContainer.empty(); // Clear the container

        if (feedback.length === 0) {
            feedbackContainer.append('<p>No feedback available for this product.</p>');
        } else {
            feedback.forEach(f => {
                const feedbackElement = `
                    <div class="feedback-item">
                        <p><strong>User ${f[1]}:</strong> ${f[4]}</p>
                        <p><em>Rating: ${f[3]}</em></p>
                    </div>`;
                feedbackContainer.append(feedbackElement);
            });
        }
    }

    // Fetch and display existing feedbacks
    $.getJSON(`/feedback?product_id=${productId}`, function(data) {
        if (data.message !== "No feedback found for this product") {
            renderFeedback(data);
        } else {
            $('#feedback-container').append('<p>No feedback available for this product.</p>');
        }
    });

    // Handle new feedback submission
    $('#feedback-form').on('submit', function(event) {
        event.preventDefault();

        const feedbackData = {
            product_id: productId,
            user_id: $('#user-id').val(),  // assuming you have a way to get the user's ID
            rating: $('#rating').val(),
            comment: $('#comment').val()
        };

        $.ajax({
            type: 'POST',
            url: '/feedback',
            contentType: 'application/json',
            data: JSON.stringify(feedbackData),
            success: function(response) {
                alert("Thank you for your feedback!");
                location.reload(); // Reload page to see the new feedback
            },
            error: function(xhr) {
                alert("Failed to submit feedback");
            }
        });
    });
});
$(document).ready(function(){
    const user_exists = localStorage.getItem("user_id");
    $("#log_out").click(function(){
        localStorage.clear()
        location.reload()
    })
    if(user_exists){
        const logged_in = document.getElementById('logged_in');
        const log_out = document.getElementById('log_out');
        logged_in.style.display= 'none';
        log_out.style.display = 'block';

        document.getElementById("cart_items_total").innerHTML = JSON.parse(localStorage.getItem('cart')).length
    }
    if (!user_exists){
        const logged_in = document.getElementById('logged_in');
        const log_out = document.getElementById('log_out');
        logged_in.style.display= 'block';
        log_out.style.display = 'none';
        localStorage.clear()
    }
}) 