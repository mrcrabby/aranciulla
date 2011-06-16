$(function(){

function hide_keyword(){
	$(this).hide("slow");
	$(this).nextAll().each(function(index,value){
		if($(value).attr("class") == 'even'){
			$(value).removeClass('even');
			$(value).addClass('odd');
		}
		else {
			$(value).removeClass('odd');
			$(value).addClass('even');
		}
	});
}

$('.muovi_scritti').click(function() {
	var keyword = $(this).attr('keyword');
	$.ajax({
		url: "/scritto?keyword="+keyword,
		context:$(this).parent().parent(),
		success: hide_keyword
	});
});

$('.muovi_bloccati').click(function() {
	var keyword = $(this).attr('keyword');
	$.ajax({
		url: "/bloccato?keyword="+keyword,
		context:$(this).parent().parent(),
		success: hide_keyword
	});
});

$('.muovi_back').click(function() {
	var keyword = $(this).attr('keyword');
	$.ajax({
		url: "/back?keyword="+keyword,
		context:$(this).parent().parent(),
		success: hide_keyword
	});
});

});

