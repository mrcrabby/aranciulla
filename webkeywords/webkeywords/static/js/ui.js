$(document).ready(function() {

	$('ul.items>li.active>ul').slideDown();

	
	$(function() {
			   
		$('.items').click(clickFn);
		
	});
	
	function clickFn(e) {
		
		var $el = $(e.target);
		if (!$el.parent().children('ul').is(':visible')) {
			
			if ($el.parent().parent().is('ul.items')) {
				
				var $visibles=$('ul.items>li>ul:visible');
				if ($visibles.length>0){
					$visibles.slideUp('medium', function(){
						 $el.parent().children("ul").slideDown('slow');
						}
					);
				}
				else{
					$el.parent().children("ul").slideDown('slow');
				}

			}
			
		}
	
	}	

	function getEventTarget(e) {
		
		e = e || window.event;
		return e.target || e.srcElement;
		
	}

	$('.close').click(function() {
									 
		$(this).parents(".alert").animate({ opacity: 'hide' }, "slow");
		return false;
		
	});
	
	$(document).keyup(function(event) {
		if (event.keyCode == 13) {
			$(this).parents("form").submit();
			return false;
		}
	});
	
	$('.submit').click(function() {
									 
		$(this).parents("form").submit();
		return false;
		
	});
	
	
	$("#keyword-tree").jstree({ 
		"json_data" : {
			"ajax" : {
				"url": "url",
				}
			},
		"plugins" : [ "themes", "json_data" ]
	});
	


});
