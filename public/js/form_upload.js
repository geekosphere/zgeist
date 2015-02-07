
(function () {
  var element = $('textarea#urls');
  if (element.length == 0) return;
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

