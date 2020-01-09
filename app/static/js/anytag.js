$(document).ready(function () {
    $('#newTodo').trigger('focus')
    $('#listSelector').on('change', switchList)
  });

function switchList(){
  var url = $('#listSelector').val();
  if (url && url.length){
    location.href = url;
  }
}