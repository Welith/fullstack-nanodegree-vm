$(document).ready(function () {
    // Restaurant ajaxes
    $('#editRes_').on('click', function (e) {
        var id = $('#editRes_').data('id'), name = $('name').val();
        e.preventDefault();
        $.ajax({
            url: "/restaurants/" + id + "/edit",
            method: 'post',
            data: $('.form-signin').serialize(),
            success: function () {
                console.log('Success')
                location.reload()
            },
            error: function() {
                console.log('Error')
            }
        });
    });
    $('#deleteRes_').on('click', function (e) {
        var id = $('#deleteRes_').data('id');
        console.log(id);
        e.preventDefault();
        $.ajax({
            url: "/restaurants/" + id + "/delete",
            method: 'post',
            success: function () {
                console.log('Success')
                location.reload()
            },
            error: function() {
                console.log('Error')
            }
        });
    });
    $('#addRes_').on('click', function (e) {
        e.preventDefault();
        $.ajax({
            url: "/restaurants/add",
            method: 'post',
            data: $('.form-new').serialize(),
            success: function () {
                console.log('Success')
                location.reload()
            },
            error: function() {
                console.log('Error')
            }
        });
    });
    // Menu Items ajaxes
    $('#editIt_').on('click', function (e) {
        var id = $('#editIt_').data('id'), restaurant_id = $('#editIt_').data('restaurant');
        e.preventDefault();
        $.ajax({
            url: "/restaurants/" + restaurant_id + "/item/" + id + "/edit",
            method: 'post',
            data: $('.form-signin').serialize(),
            success: function () {
                console.log('Success')
                location.reload()
            },
            error: function() {
                console.log('Error')
            }
        });
    });
    $('#deleteIt_').on('click', function (e) {
        var id = $('#deleteIt_').data('id'), restaurant_id = $('#deleteIt_').data('restaurant');
        e.preventDefault();
        $.ajax({
            url: "/restaurants/" + restaurant_id + "/item/" + id + "/delete",
            method: 'post',
            success: function () {
                console.log('Success')
                location.reload()
            },
            error: function() {
                console.log('Error')
            }
        });
    });
    $(".alert-success").fadeTo(2000, 1000).slideUp(1000, function () {
        $(".alert-success").slideUp(1000);
    });
});