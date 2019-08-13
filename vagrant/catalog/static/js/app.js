$(document).ready(function () {

    // Menu Items ajaxes
    var $itemId = $('#mainEditButton').data('itemid'), $itemName = $('#mainEditButton').data('itemname'), 
    $editAction = $('#mainEditButton').data('action'), $categoryId = $('#mainEditButton').data('catid');
    $('#editModalLabel').html('Edit item ' + $itemName)
    $('#editItemForm').attr('action', $editAction)
    $('#editName').attr('placeholder', $itemName)
    $('#editIt').on('click', function (e) {
        e.preventDefault();
        $.ajax({
            url: "/categories/" + $categoryId + "/items/" + $itemId + "/edit",
            method: 'post',
            data: $('#editItemForm').serialize(),
            success: function () {
                console.log('Success')
                location.reload()
            },
            error: function () {
                console.log('Error')
            }
        });
    });
    var $itemDelId = $('#mainDeleteButton').data('itemid'), $restDelId = $('#mainDeleteButton').data('restid'),
        $itemDelName = $('#mainDeleteButton').data('itemname'), $deleteAction = $('#mainDeleteButton').data('action');
    $('#deleteModalLabel').html('Edit item ' + $itemDelName)
    $('#deleteItemForm').attr('action', $deleteAction)
    $('#deleteName').attr('placeholder', $itemDelName)
    $('#deleteIt').on('click', function (e) {
        e.preventDefault();
        $.ajax({
            url: "/restaurants/" + $restDelId + "/item/" + $itemDelId + "/delete",
            method: 'post',
            success: function () {
                console.log('Success')
                location.reload()
            },
            error: function () {
                console.log('Error')
            }
        });
    });
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
    }
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