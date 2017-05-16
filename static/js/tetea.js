var setSelect = function(lastSelect,fxn,thisSelect) {
	var typeSelect = document.getElementById(lastSelect);
	var typePicked = typeSelect.options[typeSelect.selectedIndex].text;
	var topics = ""
	$.ajax({
		traditional: true,
		//async: false,
        type: "GET",
        url: fxn,
        data: {category: typePicked},
        dataType: "text",
        success: function(response){
        	topics = response
        },
        error: function(textStatus, errorThrown){
        	console.log(textStatus)
        	console.log(errorThrown)
        }
	})
	.done(function() {
		var topicList = topics.split(",")
		var select = document.getElementById(thisSelect);
		// clear old subtopics
		while (select.hasChildNodes()) {
			select.removeChild(select.lastChild);
		}

		var i=0;
		for (i=0; i<topicList.length; i++){
			var node = document.createElement("option");
			node.setAttribute("value", topicList[i])
			node.innerHTML = topicList[i]
			select.appendChild(node)
		}
	});
};

var setTopics = function() {
	setSelect("selectTypes","/getTopics/","selectTopics");
}

var setSubtopics = function() {
	setSelect("selectTopics","/getSubtopics/","selectSubtopics")
}