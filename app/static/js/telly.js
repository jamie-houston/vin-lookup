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

function formatDealer(value, row, index){
    return "<a href='/dealer/"+value+"'>"+value+"</a>";
}

function formatVin(value, row, index){
    return "<a href='/car/"+value+"'>"+value+"</a>";
}
