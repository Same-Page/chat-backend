var chat_url = "wss://7dvmt9p591.execute-api.ap-southeast-1.amazonaws.com/prod"

var ws = new WebSocket(chat_url)

ws.onopen = function() {
	// const payload = {
	// 	action: "message",
	// 	data: "hithrere"
	// }
	// ws.send(payload)
	// console.log("Message is sent...")
}

ws.onmessage = function(evt) {
	var received_msg = evt.data

	console.log("Message is received...")
	console.log(received_msg)
}

ws.onclose = function() {
	// websocket is closed.
	alert("Connection is closed...")
}

function sendMessage() {
	const payload = {
		action: "message",
		data: {
			name: "David",
			age: 10
		}
	}
	ws.send(JSON.stringify(payload))
}
function joinRoom() {
	const payload = {
		action: "join",
		data: {
			url: "g.com"
		}
	}
	ws.send(JSON.stringify(payload))
}
