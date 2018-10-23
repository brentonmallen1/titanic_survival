// This function will run to enhance the user's experience

$(function() {
    // handle the decoder buttons
    $('input[type="submit"]').click(function(event) {  // tell this function to operate on all 'input' elements of type 'submit'.
        var $form = $(this).parent();  // this is the object that triggered the event, in this case = the form submit button
        $form.find('.output').text("")
        $.ajax({
            url: $form.attr('action'),  // search the form for the 'action' attribute and point the url to that value
            data: $form.serialize(),  //  send the entire form, serialized, to the url endpoint
            type: 'POST',  // send as a post request
            success: function(response) {  // handle the response if successful
                // parse the json string into a json object and pretty print it using strigify
                $form.find('.output').text(JSON.stringify(JSON.parse(response), null, 2))
                // send the successful response to the output div in the form
                console.log(response);  // log the response to the browser console
            },
            error: function(error) {  // handle the response if there's an error
                // send the error to the page
                $form.find('.output').text(error.responseText)
                console.log(error);  // log the error to the console
            }
        });
        event.preventDefault()  // prevents browser from triggering submit and going to the endpoint page (see below)
    });
});

// normally the browser will want to load the new page, with `preventDefault()` we're preventing that behavior so we can
// load the response dynamically on the page