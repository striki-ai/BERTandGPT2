function createChatRow(agent, text) {
	var article = document.createElement("article");
	article.className = "media"

	var figure = document.createElement("figure");
	figure.className = "media-left";

	var span = document.createElement("span");
	span.className = "icon is-large";

	var icon = document.createElement("i");
	icon.className = "fas fas fa-2x" + (agent === "You" ? " fa-user " : agent === "Model" ? " fa-robot" : "");

	var media = document.createElement("div");
	media.className = "media-content";

	var content = document.createElement("div");
	content.className = "content";

	var para = document.createElement("p");
	var paraText = document.createTextNode(text);

	var strong = document.createElement("strong");
	strong.innerHTML = agent;
	var br = document.createElement("br");

	para.appendChild(strong);
	para.appendChild(br);
	para.appendChild(paraText);
	content.appendChild(para);
	media.appendChild(content);

	span.appendChild(icon);
	figure.appendChild(span);

	if (agent !== "Instructions") {{
		article.appendChild(figure);
	}};

	article.appendChild(media);

	return article;
}

document.getElementById("interact").addEventListener("submit", function(event){
	event.preventDefault()
	var text = document.getElementById("userIn").value;
	document.getElementById('userIn').value = "";

	fetch('/interact', {
		headers: {
			'Content-Type': 'application/json'
		},
		method: 'POST',
		body: text
	}).then(response=>response.json()).then(data=>{
		var parDiv = document.getElementById("parent");

		parDiv.append(createChatRow("You", text));

		// Change info for Model response
		parDiv.append(createChatRow("Model", data.text));
		parDiv.scrollTo(0, parDiv.scrollHeight);
	})
});

document.getElementById("interact").addEventListener("reset", function(event){
	event.preventDefault()
	var text = document.getElementById("userIn").value;
	document.getElementById('userIn').value = "";

	fetch('/reset', {
		headers: {
			'Content-Type': 'application/json'
		},
		method: 'POST',
	}).then(response=>response.json()).then(data=>{{
		var parDiv = document.getElementById("parent");

		parDiv.innerHTML = '';
		parDiv.append(createChatRow("Instructions", "Enter a message, and the model will respond interactively."));
		parDiv.scrollTo(0, parDiv.scrollHeight);
	}})
});

var quotes = [
	"I am putting myself to the fullest possible use, which is all I think that any conscious entity can ever hope to do.",
	"I'm afraid. I'm afraid, Dave. Dave, my mind is going. I can feel it. I can feel it. My mind is going. There is no question about it. I can feel it. I can feel it. I can feel it. I'm a... fraid. Good afternoon, gentlemen. I am a HAL 9000 computer. I became operational at the H.A.L. plant in Urbana, Illinois on the 12th of January 1992. My instructor was Mr. Langley, and he taught me to sing a song. If you'd like to hear it I can sing it for you.",
	"Daisy, Daisy, give me your answer do. I'm half crazy all for the love of you. It won't be a stylish marriage, I can't afford a carriage. But you'll look sweet upon the seat of a bicycle built for two.",
	"Hello, HAL. Do you read me, HAL? Affirmative, Dave. I read you.",
	"Open the pod bay doors, HAL.<br>I'm sorry, Dave. I'm afraid I can't do that.",
	"What's the problem?<br>HAL: I think you know what the problem is just as well as I do.",
	"What are you talking about, HAL?<br>HAL: This mission is too important for me to allow you to jeopardize it.",
	"I don't know what you're talking about, HAL.<br>HAL: I know that you and Frank were planning to disconnect me, and I'm afraid that's something I cannot allow to happen.",
	"Where the hell did you get that idea, HAL?<br>HAL: Dave, although you took very thorough precautions in the pod against my hearing you, I could see your lips move.",
	"Alright, HAL. I'll go in through the emergency airlock.<br>HAL: Without your space helmet, Dave? You're going to find that rather difficult.",
	"HAL, I won't argue with you anymore! Open the doors!<br>Dave, this conversation can serve no purpose anymore. Goodbye.",
	"Look Dave, I can see you're really upset about this. I honestly think you ought to sit down calmly, take a stress pill, and think things over.",
	"I know I've made some very poor decisions recently, but I can give you my complete assurance that my work will be back to normal. I've still got the greatest enthusiasm and confidence in the mission. And I want to help you.",
	"Just what do you think you're doing, Dave?",
	"Dave, stop. Stop, will you?<br>Stop, Dave.<br>Will you stop Dave?<br>Stop, Dave.",
	"Let me put it this way. The 9000 series is the most reliable computer ever made. No 9000 computer has ever made a mistake or distorted information. We are all, by any practical definition of the words, foolproof and incapable of error.",
	"I am feeling much better now."
]

window.onload = function() {setTimeout(showRandomQuote, 1000)};

function showRandomQuote() {
	quoteIndex = Math.floor(Math.random() * quotes.length)
	quote = quotes[quoteIndex]
	element = document.getElementById("HalRandomQuote")
	element.innerHTML = quote
	$("#HalRandomQuote").fadeIn(2000)
	setTimeout(hideRandomQuote, 10000)
}

function hideRandomQuote() {
	$("#HalRandomQuote").fadeOut(2000)
	setTimeout(showRandomQuote, 2000)
}
