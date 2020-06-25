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
