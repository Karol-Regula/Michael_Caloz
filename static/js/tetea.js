//gets selected of dropdown with id thisselect
var selected = function(thisSelect) {
	var typeSelect = document.getElementById(thisSelect);
	var typePicked = typeSelect.options[typeSelect.selectedIndex].text;
	return typePicked;
}

// Updates thisSelect menu based on the choice
// made in the lastSelect menu (using the function fxn)
// NOT USING RN, keeping for ajax
var setSelect = function(lastSelect,fxn,thisSelect) {
	var typePicked = selected(lastSelect);
	var topics = ""
	// run fxn, set topics to response
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
		// once done, set dropdown to topics
		setDropdown(topics, thisSelect);
	});
};

// resets dropdown with id thisSelect to contain
// the information in to_add (which is either values
// separated by commas, or an array)
var setDropdown = function(to_add, thisSelect) {
	if (to_add instanceof String) {
		// str of comma separated vals
		var topicList = to_add.split(",");
	} else {
		// just use the array as is
		var topicList = to_add;
	}
	
	var select = document.getElementById(thisSelect);
	// clear old subtopics
	while (select.hasChildNodes()) {
		select.removeChild(select.lastChild);
	}

	//add each item in list to dropdown
	var i=0;
	for (i=0; i<topicList.length; i++){
		var node = document.createElement("option");
		node.setAttribute("value", topicList[i])
		node.innerHTML = topicList[i]
		select.appendChild(node)
	}
};

//sets topics when form data is changed
var setTopics = function(topics) {
	var subjPicked = selected("selectSubjects");
	var typePicked = selected("selectTypes");

	if (typePicked=='Notes') {
		//set topics based on subject
		setDropdown(topics[subjPicked], "selectTopics");
	} else {
		//no topics: clear the dropdown of options
		var select = document.getElementById("selectTopics");
		while (select.hasChildNodes()) {
			select.removeChild(select.lastChild);
		}
	}
};

// Runs upon submission
// Gets content based on subj/type/topic
var getContent = function() {
	var subj = selected("selectSubjects");
	var mType = selected("selectTypes");
	var mTopic;
	//only get type if applicable
	if (mType=='Notes') {
		mTopic = selected("selectTopics");
	} else {
		mTopic = "";
	}

	// call to app.py to get the content
	$.ajax({
		traditional: true,
        type: "GET",
        url: "/getContent/",
        data: {subject: subj, type: mType, topic: mTopic},
        dataType: "text",
        success: function(response){
        	console.log(response)
        },
        error: function(textStatus, errorThrown){
        	console.log(textStatus)
        	console.log(errorThrown)
        }
	})
	.done(function() {
		console.log("done!")
		// add content to page
	});
}