/**
 * Created by Michael on 23/07/2015.
 */

function SubmitForm(form_id) {

        var frm = $(form_id);
        frm.submit(function (e) {
            e.preventDefault();
            $.ajax({
                type: frm.attr('method'),
                url: frm.attr('action'),
                data: frm.serialize(),
                success: function (data) {
                    setPopup('alert-success', data['message']);
                    console.log(data['message']);
                },
                error: function(data) {
                    setPopup('alert-danger', "Something went wrong!");
                }
            });
            return false;
        });
}