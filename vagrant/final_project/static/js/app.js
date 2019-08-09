$(document).ready(function () {
    // Restaurant ajaxes
    var resId = $('#mainEditButton').data('id'), resName = $('#mainEditButton').data('name'),
        formAction = $('#mainEditButton').data('action');
    $('#editModalLabel').html('Edit Restaurant ' + resName);
    $('#editForm').attr('action', formAction);
    $('#name').attr('placeholder', resName);
    $('#editRes').on('click', function (e) {
        e.preventDefault();
        $.ajax({
            url: "/restaurants/" + resId + "/edit",
            method: 'post',
            data: $('#editForm').serialize(),
            success: function () {
                console.log('Success')
                //location.reload()
            },
            error: function () {
                console.log('Error')
            }
        });
    });

    var deleteResId = $('#mainDeleteButton').data('id'), deleteResName = $('#mainDeleteButton').data('name'),
        deleteFormAction = $('#mainDeleteButton').data('action');
    $('#deleteModalLabel').html('Edit Restaurant ' + deleteResName);
    $('#deleteForm').attr('action', deleteFormAction);
    $('#deleteRes').on('click', function (e) {
        e.preventDefault();
        $.ajax({
            url: "/restaurants/" + deleteResId + "/delete",
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
    $('#addRes').on('click', function (e) {
        e.preventDefault();
        $.ajax({
            url: "/restaurants/add",
            method: 'post',
            data: $('.form-new').serialize(),
            success: function () {
                console.log('Success')
                location.reload()
            },
            error: function () {
                console.log('Error')
            }
        });
    });
    // Menu Items ajaxes
    var $itemId = $('#mainEditButton').data('itemid'), $restId = $('#mainEditButton').data('restid'),
        $itemName = $('#mainEditButton').data('itemname'), $editAction = $('#mainEditButton').data('action');
    $('#editModalLabel').html('Edit item ' + $itemName)
    $('#editItemForm').attr('action', $editAction)
    $('#editName').attr('placeholder', $itemName)
    $('#editIt').on('click', function (e) {
        e.preventDefault();
        $.ajax({
            url: "/restaurants/" + $restId + "/item/" + $itemId + "/edit",
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
});