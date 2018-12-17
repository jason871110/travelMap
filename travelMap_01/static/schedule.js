/*
$('#day_1').click(function(){
  console.log("in");
  $('#empty_space').css('background-image','url(https://images.pexels.com/photos/346766/pexels-photo-346766.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940)');
});
*/
var num=3;
$('#plus_button').click(function(){
  $('#demo3').append('<a href="javascript:;" class="list-group-item" id="sche_day_1_'+num+'">num'+num+'</a>');
  num++;
})
 $('button').click(){
            $.ajax({
              url: './',
              success: function(){
                alert('success');
              },
              failure: function(){
                alert('fail');
              }
            });
          }