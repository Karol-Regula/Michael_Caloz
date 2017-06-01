//gets selected of dropdown with id thisselect
var selected_old = function(thisSelect) {
  console.log(thisSelect);
	var typeSelect = document.getElementById(thisSelect);
	var typePicked = typeSelect.options[typeSelect.selectedIndex].text;
	return typePicked;
}

//gets selected of dropdown with id thisselect
var selected = function(thisSelect) {
	//console.log("selected");
 	//console.log("thisSelect: ".concat(thisSelect));
	var typeSelect = document.getElementById(thisSelect);
	var typePicked = typeSelect.getAttribute("picked");
	//console.log(typePicked);
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
var setDropdown_old = function(to_add, thisSelect) {
	//console.log("setDropdown:" + String(to_add) + String(thisSelect))
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

var setDropdown = function(to_add, thisSelect) {
	if (to_add instanceof String) { // str of comma separated vals
		var topicList = to_add.split(",");
	} else {
		var topicList = to_add;
	}

	// var drpdwn = document.createElement("dropdown");
	// 
	// var button = document.createElement("button");
	// button.setAttribute("class","btn btn-primary dropdown-toggle");
	// button.setAttribute("type","button");
	// button.setAttribute("data-toggle","dropdown");
	// button.setAttribute("id", thisSelect.concat('-button'));
	// var spn = document.createElement("span");
	// spn.setAttribute("class","caret");
	// button.appendChild(spn);
	// 
	// var list = document.createElement("ul");
	// list.setAttribute("class", "dropdown-menu");
	// list.setAttribute("id","thisSelect");
	
	var thisSelectFull = thisSelect.concat('-inner');
	var list = document.getElementById(thisSelectFull);
	var i=0;
	for (i=0; i<topicList.length; i++){
		var listItem = document.createElement("li");
		var link = document.createElement("a");
		link.setAttribute("href","#");
		link.setAttribute("class", "link".concat(thisSelect));
		link.innerHTML = topicList[i];
		listItem.appendChild(link);
		list.appendChild(listItem);
	}
	//drpdwn.appendChild(list);
}

//sets topics when form data is changed
var setTopics = function(topics) {
	//console.log("setTopics: " + String(topics));
	topics = JSON.parse(topics);
	var subjPicked = selected("selectSubjects");
	var typePicked = selected("selectTypes");
	var select = document.getElementById("selectTopics-inner");
	var selectOuter = document.getElementById("selectTopics");
	var selectHeading = document.getElementById("selectTopicsHeading");

	if (typePicked=='Notes') {
		//set topics based on subject
		
		while (select.hasChildNodes()) {
			select.removeChild(select.lastChild);
		}
		
		var caret = document.createElement('span');
		caret.setAttribute('class', 'caret');
		selectOuter.appendChild(caret);
		selectOuter.style.display = "block";
		selectHeading.style.display = "block";
		//console.log(subjPicked);
		//console.log("setTopics[subjPicked]: " + String(topics[subjPicked]));
		setDropdown(topics[subjPicked], "selectTopics");
	} else {
		//no topics: clear the dropdown of options
		while (select.hasChildNodes()) {
			select.removeChild(select.lastChild);
		}
		var caret = document.createElement('span');
		caret.setAttribute('class', 'caret');
		selectOuter.innerHTML = "Pick a topic ";
		selectOuter.appendChild(caret);
		selectOuter.style.display = "none";
		selectHeading.style.display = "none";
	}
};

//sets quizzes when form data is changed
var setQuiz = function() {
	var subjPicked = selected("selectSubjects");
	var typePicked = selected("selectTypes");
	var quiz = document.getElementById("selectQuiz-inner");
	var quizOuter = document.getElementById("selectQuiz");
	var quizHeading = document.getElementById("selectQuizHeading");
	
	var subj = selected("selectSubjects");
	
	if (typePicked=='Questions') {
		//console.log("setQuiz:");
		var caret = document.createElement('span');
		caret.setAttribute('class', 'caret');
		quizOuter.appendChild(caret);
		quizOuter.style.display = "block";
		quizHeading.style.display = "block";
		
		while (quiz.hasChildNodes()) {
			quiz.removeChild(quiz.lastChild);
		}
		
		$.ajax({
			traditional: true,
					type: "GET",
					url: "/getQuizAmount/",
					data: {subject: subj},
					dataType: "text",
					success: function(response){
						//console.log("SucessQuiz: " + response);
						var amounts = [];
						var i = 1;
						if (response.length==0) {
							alert("No quizzes available based on your selections.");
							return ;
						}
						while (i <= parseInt(response)){
							amounts.push(i);
							i++;
						}
						setDropdown(amounts, "selectQuiz");
					},
					error: function(textStatus, errorThrown){
						console.log(textStatus)
						console.log(errorThrown)
					}
		})
		
	} else {
		while (quiz.hasChildNodes()) {
			quiz.removeChild(quiz.lastChild);
		}
		var caret = document.createElement('span');
		caret.setAttribute('class', 'caret');
		quizOuter.innerHTML = 'Pick a quiz ';
		//quizOuter.appendChild(caret);
		quizOuter.style.display = "none";
		quizHeading.style.display = "none";
	}
};


//sets definition sets when form data is changed
var setDefinition = function() {
	var subjPicked = selected("selectSubjects");
	var typePicked = selected("selectTypes");
	var definition = document.getElementById("selectDefinition-inner");
	var definitionOuter = document.getElementById("selectDefinition");
	var definitionHeading = document.getElementById("selectDefinitionHeading");
	
	var subj = selected("selectSubjects");
	
	if (typePicked=='Definitions') {
		//console.log("setDefinition:");
		var caret = document.createElement('span');
		caret.setAttribute('class', 'caret');
		definitionOuter.appendChild(caret);
		definitionOuter.style.display = "block";
		definitionHeading.style.display = "block";
		
		while (definition.hasChildNodes()) {
			definition.removeChild(definition.lastChild);
		}
		
		$.ajax({
			traditional: true,
					type: "GET",
					url: "/getDefinitionAmount/",
					data: {subject: subj},
					dataType: "text",
					success: function(response){
						//console.log("SucessDefinition: " + response);
						var amounts = [];
						console.log(response);
						if (response==0) {

							definitionOuter.style.display = "none";
							definitionHeading.style.display = "none";
							//definitionHeading.innerHTML = "No definitions available based on your selections.";
							definitionOuter.appendChild(document.createElement("br"));
    						var msg = document.createElement("p");
    						msg.innerHTML = "No notes available based on your selections.";
    						definitionOuter.appendChild(msg);
    						return ;
						}

						var i = 1;
						while (i <= parseInt(response)){
							amounts.push(i);
							i++;
						}
						setDropdown(amounts, "selectDefinition");
					},
					error: function(textStatus, errorThrown){
						console.log(textStatus)
						console.log(errorThrown)
					}
		})
		
	} else {
		while (definition.hasChildNodes()) {
			definition.removeChild(definition.lastChild);
		}
		var caret = document.createElement('span');
		caret.setAttribute('class', 'caret');
		definitionOuter.innerHTML = 'Pick a definition set ';
		definitionOuter.appendChild(caret);
		definitionOuter.style.display = "none";
		definitionHeading.style.display = "none";
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
	var mNumber;
	//only get number if applicable
	if (mType=='Questions') {
		mNumber = selected("selectQuiz");
	} else if (mType=='Definitions') {
		mNumber = selected("selectDefinition");
	} else {
		mNumber = "";
	}

	// call to app.py to get the content
	if (mNumber == ""){
	$.ajax({
		traditional: true,
        type: "GET",
        url: "/getContent/",
        data: {subject: subj, type: mType, topic: mTopic},
        dataType: "text",
        success: function(response){
        	response = JSON.parse(response)
        	if (mType=='Notes') {
        	    //displayNotes(response);
		    dispn(response);
        	} else if (mType=='Questions') {
        		//displayQuestions(response);
		    dispq(reponse);
        	} else if (mType=='Definitions') {
        	    //displayDefinitions(response);
		    dispd(response);
        	}
        },
        error: function(textStatus, errorThrown){
        	console.log(textStatus)
        	console.log(errorThrown)
        }
	})
}else{
	if (mType == "Questions"){
	$.ajax({
		traditional: true,
        type: "GET",
        url: "/getQuiz/",
        data: {subject: subj, number:mNumber},
        dataType: "text",
        success: function(response){
        	response = JSON.parse(response)
			//		console.log(response)
			//displayQuestions(response);
	    dispq(response);
        },
        error: function(textStatus, errorThrown){
        	console.log(textStatus)
        	console.log(errorThrown)
        }
	})
}else{
	$.ajax({
		traditional: true,
        type: "GET",
        url: "/getDefinition/",
        data: {subject: subj, number:mNumber},
        dataType: "text",
        success: function(response){
        	response = JSON.parse(response)
	    dispd(response);
        },
        error: function(textStatus, errorThrown){
        	console.log(textStatus)
        	console.log(errorThrown)
        }
	})
}
}
}

var contentCap = 10;
var contentCapNotes = 100;
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

var dispn = function(notes){
    clearContent();

    if (notes.length==0) {
    	content.appendChild(document.createElement("br"));
    	var msg = document.createElement("p");
    	msg.innerHTML = "No notes available based on your selections.";
    	content.appendChild(msg);
    	return ;
    }

    var cont = document.createElement("div");
    cont.setAttribute("class", "aNote");
    
    //header
    var row = document.createElement("ul");
    row.setAttribute("class", "notes_header");
    row.innerHTML = "Notes:";
    cont.appendChild(row);
    //explanation
    var row = document.createElement("ul");
    row.setAttribute("class", "notes_explanation");
    row.innerHTML = "Use these notes to gain a better understanding of the afformentioned topic.";
    cont.appendChild(row);
    
    var i=0;
    for(i=0; i<contentCapNotes; i++){
	if(notes[i] != null){
	    var row = document.createElement("ul");
	    row.setAttribute("class", "one_note");
	    row.innerHTML = (i+1)+". "+notes[i];
	    cont.appendChild(row);
	}
    }
    content.appendChild(cont);
    
    /*
    var i=0;
    for (i=0; i<contentCap; i++) {
	var row = document.createElement("div");
	row.setAttribute("class", "aNote");
	row.innerHTML = notes[i];

	content.appendChild(row);
	
    }
    */
}

var displayNotes = function(notes) {
	clearContent();

	var i=0;
	for (i=0; i<contentCapNotes; i++) {
		row = document.createElement("tr")
		row.appendChild(createContentNode(notes[i]));
		content.appendChild(row);
	}
}

var dispq = function(qs) {
    clearContent();

    if (qs.length==0) {
    	content.appendChild(document.createElement("br"));
    	var msg = document.createElement("p");
    	msg.innerHTML = "No questions available based on your selections.";
    	content.appendChild(msg);
    	return ;
    }

    for (i=0; i<contentCap; i++) {
	
	q = qs[i];
	
	var this_q = document.createElement("div");
	this_q.setAttribute("class","aContent");
	var answerList = document.createElement("ul");
	answerList.setAttribute("class","answerList");
	
	var keys = ['Question','A','B','C','D','E'];
	for (j=0; j<keys.length; j++) {
	    if (j==0) {
		var theq = document.createElement("p");
		theq.setAttribute("class","question");
		theq.innerHTML = (i+1)+". "+q[keys[j]];
		this_q.appendChild(theq);
	    } else {
		var thisAns = document.createElement("ul");
		thisAns.addEventListener('click', function(e) {

			var x=0;
			var lst = this.parentElement.childNodes;
			console.log(lst);
			for (x=0; x<lst.length; x++) {
				console.log(lst[x]);
				lst[x].setAttribute("style","font-style: normal;");
			}

			this.setAttribute("style","font-style: italic;");
		});
		if (keys[j] == q['Answer']) {
		    thisAns.setAttribute("class","answer right");
		} else {
		    thisAns.setAttribute("class","answer wrong");
		}
		var letters = ['a', 'b', 'c', 'd', 'e']
		thisAns.innerHTML = letters[j-1]+") "+q[keys[j]];
		answerList.appendChild(thisAns);
	    }
	}
	this_q.append(answerList);
	content.appendChild(this_q);
    }
}

var scoreQuiz = function() {
	var qs = document.getElementsByClassName("aContent");
	var score = 0;

	var i=0;
	for (i=0; i<qs.length; i++) { //for each question
		var j=0;
		q = qs[i];
		for (j=0; j<q.childNodes; j++) { //for each answer
			var ans = q[j];
			if ((ans.getAttribute("class")=="answer right") &&
				ans.getAttribute("style")=="font-style: italic;") {
				score+=1;
			}
		}
	}
	return score;
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
		console.log(q);
		var j=0;
	    for (j=0; j<keys.length; j++) {
		if(j==0){
		    var item = createContentNode(i+1+". <br>"+q[keys[j]])
		}
		else{
		    var item = createContentNode(q[keys[j]])
		}
			if (keys[j]=='Question') {
				item.setAttribute("class","question")
			}

 			if (keys[j]==q['Answer']) { //If correct answer
 				item.addEventListener('click', function(e) { this.setAttribute("style","color: green;"); });
 				item.setAttribute("class","answer right"); //adds BOTH CLASSES to this element
 			} else if (keys[j].length==1) { //wrong answer
 				item.addEventListener('click', function(e) { this.setAttribute("style","color: red;"); });
 				item.setAttribute("class","answer wrong");
 			}
 			this_row.appendChild(item);
		}
		this_row.setAttribute("class","qitem");
		content.appendChild(this_row);
	}
}

var dispd = function(defs) {
    clearContent();

    var i=0;
    for (i=0; i<contentCap; i++) {
	def = defs[i];
	if (def==null) { break;}

	var thisOne = document.createElement("div");
	thisOne.setAttribute("class","aContent definition");
	thisOne.setAttribute("word", def['Word']);
	thisOne.setAttribute("definition", def['Definition']);
	thisOne.innerHTML = thisOne.getAttribute("word");



	
	thisOne.addEventListener('click',
				 function(e){
				     console.log(this.getAttribute("word"));
				     console.log(this.innerHTML);
				     if(this.innerHTML == this.getAttribute("word")){
					 console.log(this);
					 this.innerHTML = this.getAttribute("definition");  }
				     else{
					 console.log("else");
					 this.innerHTML = this.getAttribute("word");  }
				 });
					 
	
	content.appendChild(thisOne);
    }
}

var dispd2 = function(defs){
    clearContent();

    var hold = document.createElement("div");
    hold.setAttribute("class", "aContent");

    var row = document.createElement("tr");
    var i=0;
    var keys = ['Word', 'Definition'];
    for (i=0; i<keys.length; i++) {
	row.appendChild(createContentNode(keys[i]));
    }
    console.log(row);
    row.setAttribute("class", "def_header");
    hold.appendChild(row);
    //content.appendChild(row);

    var i=0;
    for (i=0; i<contentCap; i++) {
	var this_row = document.createElement("tr");
	d = defs[i]
	var j=0;
	
	var itemWord = createContentNode(d[keys[0]])
	var itemDef = createContentNode(d[keys[1]])
	itemDef.setAttribute("style","visibility: hidden;");
	itemDef.setAttribute("id", String(i) + "definitionActual");
	itemWord.setAttribute("id", String(i) + "definition");
	itemWord.addEventListener('click', function(e) { document.getElementById(this.getAttribute("id") + "Actual").setAttribute("style","visibility: visible;");});
	this_row.appendChild(itemWord);
	this_row.appendChild(itemDef);

	this_row.setAttribute("class", "defs");
	
	hold.appendChild(this_row);
    }

    content.appendChild(hold);
    
    //console.log("displaying Definitions");
}

var displayDefinitions = function(defs) {
	clearContent();
	
	var row = document.createElement("tr");
	var i=0;
	var keys = ['Word', 'Definition'];
	for (i=0; i<keys.length; i++) {
		row.appendChild(createContentNode(keys[i]));
	}
	console.log(row);
	content.appendChild(row);

	var i=0;
	for (i=0; i<contentCap; i++) {
		var this_row = document.createElement("tr");
		d = defs[i]
		var j=0;
		
		var itemWord = createContentNode(d[keys[0]])
		var itemDef = createContentNode(d[keys[1]])
		itemDef.setAttribute("style","visibility: hidden;");
		itemDef.setAttribute("id", String(i) + "definitionActual");
		itemWord.setAttribute("id", String(i) + "definition");
		itemWord.addEventListener('click', function(e) { document.getElementById(this.getAttribute("id") + "Actual").setAttribute("style","visibility: visible;");});
		this_row.appendChild(itemWord);
		this_row.appendChild(itemDef);
		content.appendChild(this_row);
	}
	
	console.log("displaying Definitions");
}

function dropdown(val) {
  //var y = document.getElementsByClassName('btn btn-primary dropdown-toggle');
 	//var val = y.innerHTML;
 	//console.log(val);
 	//console.log(y);
  //var aNode = y[0].innerHTML = val + ' <span class="caret"></span>';
}

var addDropListeners = function() {
	var dropdowns = document.getElementsByClassName("dropdown-menu");
	var i;
	for (i=0; i<dropdowns.length; i++) {
		var drpdwn = dropdowns[i];
		var dropId = drpdwn.getAttribute("id");
		if (dropId.substring(0,6)=="select") {
			$(dropdown).on('click', '#'.concat(dropId).concat(' li a'), function() {
				console.log(dropId);
				var id = "select".concat(this.getAttribute("class").substring(4));
				if (id != "selectSubjects" && id != "selectTypes"){
					id = this.getAttribute("class").substring(4);
				}
				console.log('id: '.concat(id));
    		var button = document.getElementById(id);
    		button.innerHTML = $(this).text();
    		button.setAttribute("picked",$(this).text());
				setTopics(document.getElementById('topicSource').innerHTML);
				setQuiz();
				setDefinition();
				//addDropListeners();
    		});
		}
	}
}

window.onload = function WindowLoad(event) {
	var select = document.getElementById("selectTopics");
	var selectHeading = document.getElementById("selectTopicsHeading");
	select.style.display = "none";
	selectHeading.style.display = "none";

	var quiz = document.getElementById("selectQuiz");
	var quizHeading = document.getElementById("selectQuizHeading");
	quiz.style.display = "none";
	quizHeading.style.display = "none";

	var definition = document.getElementById("selectDefinition");
	var definitionHeading = document.getElementById("selectDefinitionHeading");
	definition.style.display = "none";
	definitionHeading.style.display = "none";

	addDropListeners();
}
