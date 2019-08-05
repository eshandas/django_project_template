//-----------------------------------------------------------------------------------------------//

/* Custom AJAX POST method to avoid http 403 as csrf token needs to be copied before sending the request
 Use this method to POST data (in case you arent using form for the post)
 Inputs: url > same domain url
        data > no string, only JSON Object
        success > a function which provides as a return point if POST is a success
        error > a function which provides as a return point if POST is a failure
 e.g:post_with_csrf("/company/recruiter/apply_for_job/",
                   {'hdnJobPostingId': hdnJobPostingId},
                   function(json) {
                        showNotification(json.message);
                    },
                    function(xhr,errmsg,err) {
                        console.log(xhr.status + ": " + xhr.responseText);
                    });
*/
function post_with_csrf(url, data, success, error){
    $.ajax({
        url : url,
        type : "POST",
        dataType: "json",
        data : JSON.stringify(data),
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
        },
        success : success,
        error : error
    });
};

function get_with_csrf(url, success, error){
    $.ajax({
        url : url,
        type : "GET",
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
        },
        success : success,
        error : error
    });
};

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};


//-----------------------------------------------------------------------------------------------//
$(document).ready(function() {
    // Select shopify store
    $('#selectShopifyStore').change(function() {
        var shopifyStoreId = $('#selectShopifyStore').val();
        var previousShopifyStore = $('#previousShopifyStore').val();
        if(shopifyStoreId != '0') {
            var switchToShopifyStoreUrl = $('#switchToShopifyStoreUrl').val();
            switchToShopifyStoreUrl += '?switchTo=' + shopifyStoreId + '&previousShopifyStore=' + previousShopifyStore + '&next=' + window.location.href;
            var selected_text = $("#selectShopifyStore option:selected").text();
            var modal = $('#siteModal');

            modal.find('.modal-header').html('');
            modal.find('.modal-body').html('');
            modal.find('.modal-footer').html('');

            modal.find('.modal-header').append('<h4 class="modal-title">Change Shopify Store</h4>');
            modal.find('.modal-body').append('<p>You are switching to another Shopify Store: ' + selected_text + '</p>');
            var footer = '<a type="button" class="btn btn-outline btn-info" href="' + switchToShopifyStoreUrl + '">Accept</a>'
            footer += '<button type="button" class="btn btn-outline btn-info" data-dismiss="modal">Close</button>';
            modal.find('.modal-footer').append(footer);
            modal.modal();
        };
    });

    // Display alerts when lpage loads, if any
    if($('#alertMessage').length > 0) {
        new PNotify({
            title: $('#alertTitle').val(),
            text: $('#alertMessage').val(),
            type: $('#alertMessageType').val(),
            shadow: true
        });
    };
});