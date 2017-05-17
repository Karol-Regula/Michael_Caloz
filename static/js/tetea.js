// Updates thisSelect menu based on the choice
// made in the lastSelect menu (using the function fxn)
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
		setDropdown(topics, thisSelect);
	});
};

var setDropdown = function(to_add, thisSelect) {
	if (to_add instanceof String) {
		var topicList = to_add.split(",");
	} else {
		var topicList = to_add;
	}
	
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
};


var setTopics = function(topics) {
	var subjSelect = document.getElementById("selectSubjects");
	var subjPicked = subjSelect.options[subjSelect.selectedIndex].text;

	var typeSelect = document.getElementById("selectTypes");
	var typePicked = typeSelect.options[typeSelect.selectedIndex].text;

	if (typePicked=='Notes') {
		setDropdown(topics[subjPicked], "selectTopics");
	} else {
		var select = document.getElementById("selectTopics");
		while (select.hasChildNodes()) {
			select.removeChild(select.lastChild);
		}
	}
};