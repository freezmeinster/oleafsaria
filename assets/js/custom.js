$(function () {
	$('.caption').popover({
		placement: 'bottom'
	});
	
	$('.tooltip-left').tooltip({
		placement: 'left'
	});
	
	$('.tooltip-right').tooltip({
		placement: 'right'
	});
	
	$('.tooltip-top').tooltip({
		placement: 'top'
	});
	
	$('.tooltip-bottom').tooltip({
		placement: 'bottom'
	});
	
	// Check or uncheck all checkboxes
	$('.check_all').click(function() {
		$(this).parents('form').find('input:checkbox').attr('checked', $(this).is(':checked'));   
	});

	// Tabular
    $('a[data-toggle="tab"]').on('shown', function (e) {
	    e.target;
	    e.relatedTarget;
	    $('a[data-toggle="tab"]').attr('class','btn btn-warning');
	    $(this).attr('class','active btn btn-warning');
    })
    
    $('.delete').click(function(){
    	if(confirm('Are you sure delete the selected item ?'))
    	{
    		return true;
    	} else {
    		return false;
    	}
    });
});