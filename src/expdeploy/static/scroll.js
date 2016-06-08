jQuery(document).ready(function ($) {

  $('.nav a').click(function (e) {
  e.preventDefault()
  $(this).tab('show')
})  
    
    $('a.scroll').on('click', function (e) {
        var href = $(this).attr('href');
        $('html, body').animate({
            scrollTop: $(href).offset().top
        }, 'slow');
        e.preventDefault();
    });
});