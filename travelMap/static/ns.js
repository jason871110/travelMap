$('.sortable-list').sortable({
  connectWith: '.sortable-list',
  cancel: '#unsort-item',
  update: function(event, ui) {
    var changedList = this.id;
    var order = $(this).sortable('toArray');
    var positions = order.join(';');
	  var order0,order1
	if (changedList == "Day0"){
		order0 = positions;
		$( "#order0" ).val(order0);
		$( "#pp0").text(order0);
	}
	else if(changedList == "Day1"){
	  	order1 = positions;
		$( "#order1" ).val(order1);
		$( "#pp1").text(order1);
	}
	console.log({
      order0: order0,
	  order1: order1,
    });
  }

});



/*
let items = document.querySelectorAll('#items-list >  #moveable')

items.forEach(item => {
  $(item).prop('draggable', true)
  item.addEventListener('dragstart', dragStart)
  item.addEventListener('drop', dropped)
  item.addEventListener('dragenter', cancelDefault)
  item.addEventListener('dragover', cancelDefault)
})

function dragStart (e) {
  var index = $(e.target).index()
  console.log('dragStart')
  e.dataTransfer.setData('text/plain', index)
  console.log(index)

}
function dropped (e) {
  cancelDefault(e)
  
  // get new and old index
  let oldIndex = e.dataTransfer.getData('text/plain')
  let target = $(e.target)
  let newIndex = target.index()
 
  $( "#pp" ).append( oldIndex+">"+newIndex+"  ")
  //alert($("#pp").text())
  var order = $("#pp").text()
  //alert(order)
  $( "#order" ).val(order)
  //$( "#order" ).append( oldIndex+">"+newIndex+"  ");
  // remove dropped items at old place
  if(newIndex != oldIndex){
	let dropped = $(this).parent().children().eq(oldIndex).remove()
  // insert the dropped items at new place
  if (newIndex < oldIndex) {
    target.before(dropped)
  } else {
    target.after(dropped)
  }
 }
  console.log('dragEnd')

}

function cancelDefault (e) {
  e.preventDefault()
  e.stopPropagation()
  return false
}
*/