
$(document).ready(function () {
    function loadComments() {
        $.ajax({
            url: "/comments/list/",  // Replace with the actual URL for retrieving comments
            type: "GET",
            success: function(response) {
                $("#comments-container").html(response);  // Update the comments container with the retrieved comments
                console.log("Load oke");

            },
            error: function(xhr, errmsg, err) {
                console.log("Error loading comments: " + errmsg);
            }
        });
    }

    // Load comments on page load
    loadComments();

    // Handle form submission
    $("#comment-form").submit(function(event) {
        event.preventDefault();
        var formData = $(this).serialize();

        $.ajax({
            url: $(this).attr("action"),
            type: $(this).attr("method"),
            data: formData,
            success: function(response) {
                console.log("Comment created successfully!");
                loadComments();  // Reload comments after successful creation
                $("#comment-form")[0].reset();
            },
            error: function(xhr, errmsg, err) {
                console.log("Error creating comment: " + errmsg);
            }
        });
    });
});
