$(function(){

$('.muovi_scritti').click(function() {
	var keyword = $(this).attr('keyword');
	$.ajax({
		url: "/scritto?keyword="+keyword,
		context:$(this).parent().parent(),
		success: function(){
			$(this).hide("slow");
		}
	});
});

$('.muovi_bloccati').click(function() {
	var keyword = $(this).attr('keyword');
	$.ajax({
		url: "/bloccato?keyword="+keyword,
		context:$(this).parent().parent(),
		success: function(){
			$(this).hide("slow");
		}
	});
});

});

