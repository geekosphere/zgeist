

(function () {
  var element = $('textarea#urls');
  var dynamic_rows = function (e) {
    var content = element.val();
    var rows = content.split('\n').length;
    rows++;
    if (rows > 7) rows = 7;
    if (content == '') rows = 1;
    element.attr('rows', rows);
  };
  element.change(dynamic_rows)
         .keyup(dynamic_rows);
  dynamic_rows();
})();


(function () {
  var element = $('#add-tag');


})();



  /*
_.each($('.block-toggle'), function (element) {
  element = $(element);
  var title = element.children('.block-title');   
  var body = element.children('.block-body');

  body.hide();
  title.addClass('block-title-hover')
    .click(function (e) {
      
    });
});

*/


