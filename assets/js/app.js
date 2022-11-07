(function($){
	$("#preprint-publications, #conference-publications, #journal-publications, #thesis-publications").on("click", "a.show-abstract", function(e){
		e.preventDefault();
		$(this).closest("li").find("div.abstract-details").toggleClass("hide");
	});
})(jQuery);