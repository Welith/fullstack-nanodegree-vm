$(document).ready(function () {

    // Edit item ajax
    var $itemName = $('#mainEditButton').data('itemname'),
        $editAction = $('#mainEditButton').data('action'),
        $editRedirect = $('#mainEditButton').data('redirect');
    $('#editModalLabel').html('Edit item ' + $itemName)
    $('#editItemForm').attr('action', $editAction)
    $('#editIt').on('click', function (e) {
        e.preventDefault();
        $.ajax({
            url: $editAction,
            method: 'post',
            data: $('#editItemForm').serialize(),
            success: function () {
                console.log('Success')
                location.href = $editRedirect
            },
            error: function () {
                console.log('Error')
            }
        });
    });
    // Logout ajax
    var $logoutAction = $('#mainLogoutButton').data('action'), $logoutRedirect = $('#mainLogoutButton').data('redirect');
    $('#logoutForm').attr('action', $logoutAction);
    $('#disconnect').on('click', function (e) {
        e.preventDefault();
        $.ajax({
            url: $logoutAction,
            method: "POST",
            success: function () {
                console.log('Success')
                location.href = $logoutRedirect
            },
            error: function () {
                console.log('Error')
            }
        })
    });
    // Add item ajax
    var $addAction = $('#mainAddButton').data('action'),
        $addRedirect = $('#mainAddButton').data('redirect');
    $('#addCatItemForm').attr('action', $addAction);
    $('#addIt').on('click', function (e) {
        e.preventDefault();
        $.ajax({
            url: $addAction,
            method: "POST",
            data: $('#addCatItemForm').serialize(),
            success: function () {
                console.log('Success')
                location.href = $addRedirect
            },
            error: function () {
                console.log('Error')
            }
        })
    })
    // Delete Item Ajax
    var $deleteAction = $('#mainDeleteButton').data('action'),
        $deleteRedirect = $('#mainDeleteButton').data('redirect'),
        $deleteName = $('#mainDeleteButton').data('itemname');
    $('#deleteItemForm').attr('action', $deleteAction);
    $('#deleteModalLabel').html('Are you sure you want to delete ' + $deleteName + "?")
    $('#deleteIt').on('click', function (e) {
        e.preventDefault();
        $.ajax({
            url: $deleteAction,
            method: 'POST',
            success: function () {
                console.log('Success')
                location.href = $deleteRedirect
            },
            error: function () {
                console.log('Error')
            }
        })
    })
    $(".alert-success").fadeTo(2000, 1000).slideUp(1000, function () {
        $(".alert-success").slideUp(1000);
    });
    // GOOGLE SIGN IN
    function start() {
        gapi.load('auth2', function () {
            auth2 = gapi.auth2.init({
                client_id: '288544481503-bdb12i834oanh7pk927bch6mi9jniage.apps.googleusercontent.com',
                // Scopes to request in addition to 'profile' and 'email'
                //scope: 'additional_scope'
            });
        });
    };
    start();


    $('#signinButton').click(function () {
        // signInCallback defined in step 6.
        auth2.grantOfflineAccess().then(signInCallback);
    });
    function signInCallback(authResult) {
        if (authResult['code']) {
            // Hide the sign-in button now that the user is authorized
            $('#signinButton').attr('style', 'display: none');
            $('#fbButton').attr('style', 'display: none');
            var state = $('#signinButton').data('state');
            // Send the one-time-use code to the server, if the server responds, write a 'login successful' message to the web page and then redirect back to the main restaurants page
            $.ajax({
                type: 'POST',
                url: '/gconnect?state=' + state,
                processData: false,
                data: authResult['code'],
                contentType: 'application/octet-stream; charset=utf-8',
                success: function (result) {
                    // Handle or verify the server response if necessary.
                    if (result) {
                        $('#result').html('Login Successful!</br>' + result + '</br>Redirecting...')
                        setTimeout(function () {
                            window.location.href = "/categories/";
                        }, 4000);

                    } else if (authResult['error']) {
                        console.log('There was an error: ' + authResult['error']);
                    } else {
                        $('#result').html('Failed to make a server-side call. Check your configuration and console.');
                    }
                }

            });
        }
    }
});