
//rotating among thumbs and main image
$(document).ready(function() {
	$('#thumbs img').click(function(){
		var main_src = $('#main img').attr('src');
		$('#main img').attr('src',$(this).attr('src'));
		$(this).attr('src', main_src);
	});
});
