(function($, Handlebars, undefined){

	var toChunks = function (srcArray, chunkSize) {
		var i, j, chunks = [], chunk = chunkSize || 4;
		for (i=0,j=srcArray.length; i<j; i+=chunk) {
				chunks.push(srcArray.slice(i,i+chunk));
		}
		return chunks;
	};
})(jQuery, Handlebars);