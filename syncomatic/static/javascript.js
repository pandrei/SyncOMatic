function create_folder() {
    /* This is how to wait for jQuery to load. */
    $(document).ready(function() {
        /* get form object from DOM using jQuery, search by id. */
        form = $('#create_folder');
        /* get a directory name from the user, prompt a form. */
        var dir_name = prompt("New directory name", "");
        if (dir_name && form) {
            /* get the hidden input from the form, and override his
             * value with the folder name received from user.
             */
            $(form).find('#hidden_directory_name').val(dir_name);
            /* Now that the folder name has been set, we can POST to
             * the server, requesting the folder to be created.
             */
            form.submit();
        }
    });
}

function share_folder() {
    /* This is how to wait for jQuery to load. */
    $(document).ready(function() {
        /* get the element which we want to share, that was clicked on. */
        $clicked = $(event.currentTarget);
        /* get form object from DOM using jQuery, search by id. */
        form = $clicked.siblings('form');
        /* get a email with whom to share the file/folder. */
        var share_email = prompt("Email of user you want to share this.");
        if (share_email && form) {
            /* set the email introduced by the user. */
            form.find("input[name='email']").val(share_email);
            form.submit();
        }
    });
}
