$('#post-form').on('submit',function(event){
	event.preventDefault();
	console.log("form submitted!")
	creat_post();
});
