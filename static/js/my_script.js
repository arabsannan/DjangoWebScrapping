function MyCustomFunction(){
    var loadingText = '<i class="fa fa-circle-o-notch fa-spin"></i> Capturing tweets...';

    $("#loadbtn").html(loadingText);
    //$("#btn2").attr('disabled', true);

    $(this).submit('loading').delay(1000).queue(function () {
        // $(this).button('reset');
    });

}