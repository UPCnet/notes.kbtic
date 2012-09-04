function initMenu() {
$('#menu ul').hide();

$('#menu li a').click(
   function() {
      var checkElement = $(this).next();
      if((checkElement.is('ul')) && (checkElement.is(':visible'))) {
        checkElement.slideUp('normal');
        return false;
      }
      if((checkElement.is('ul')) && (!checkElement.is(':visible'))) {
          $('#menu ul:visible').slideUp('normal');
          checkElement.slideDown('normal');
          return false;
      }
   }
);

}
$(document).ready(function() {initMenu();});