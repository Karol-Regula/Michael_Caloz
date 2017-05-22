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
	var select = document.getElementById("selectTopics");
	var selectHeading = document.getElementById("selectTopicsHeading");

	if (typePicked=='Notes') {
		//set topics based on subject
		//select.style.display = "block";
		//selectHeading.style.display = "block";
		select.style.visibility = "visible";
		selectHeading.style.visibility = "visible";
		setDropdown(topics[subjPicked], "selectTopics");
	} else {
		//no topics: clear the dropdown of options
		while (select.hasChildNodes()) {
			select.removeChild(select.lastChild);
		}
		//select.style.display = "none";
		//selectHeading.style.display = "none";
		select.style.visibility = "collapse";
		selectHeading.style.visibility = "collapse";
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
        	response = JSON.parse(response)
        	if (mType=='Notes') {
        		displayNotes(response);
        	} else if (mType=='Questions') {
        		displayQuestions(response);
        	} else if (mType=='Definitions') {
        		displayDefinitions(response);
        	}
        },
        error: function(textStatus, errorThrown){
        	console.log(textStatus)
        	console.log(errorThrown)
        }
	})
}

var contentCap = 10;
var content = null;

//clears content section of page
//so it can be filled with new content
var clearContent = function() {
	content = document.getElementById("content")
	while (content.hasChildNodes()) {
		content.removeChild(content.lastChild);
	}
}

//creates a content node given a piece of content
//modular, easy to change if we change from ul
var createContentNode = function(content) {
	var node = document.createElement("td");
	node.innerHTML = content;
	return node;
}

var displayNotes = function(notes) {
	clearContent();

	var i=0;
	for (i=0; i<contentCap; i++) {
		row = document.createElement("tr")
		row.appendChild(createContentNode(notes[i]));
		content.appendChild(row);
	}
}

var displayQuestions = function(qs) {
	clearContent();

	var row = document.createElement("tr");
	var i=0;
	var keys = ['Question','A','B','C','D','E'];
	for (i=0; i<keys.length; i++) {
		row.appendChild(createContentNode(keys[i]));
	}
	console.log(row);
	content.appendChild(row);

	var i=0;
	for (i=0; i<contentCap; i++) {
		var this_row = document.createElement("tr");
		q = qs[i]
		var j=0;
		for (j=0; j<keys.length; j++) {
			var item = createContentNode(q[keys[j]])
			if (keys[j]==q['Answer']) { //If correct answer
				item.addEventListener('click', function(e) { this.setAttribute("style","color: green;"); });
			} else if (keys[j].length==1) { //wrong answer
				item.addEventListener('click', function(e) { this.setAttribute("style","color: red;"); });
			}
			this_row.appendChild(item);
		}
		content.appendChild(this_row);
	}
}

var displayDefinitions = function(defs) {
	clearContent();
	
	console.log("displaying Definitions");
}

window.onload = function WindowLoad(event) {
	var select = document.getElementById("selectTopics");
	var selectHeading = document.getElementById("selectTopicsHeading");
	select.style.visibility = "collapse";
	selectHeading.style.visibility = "collapse";
}
