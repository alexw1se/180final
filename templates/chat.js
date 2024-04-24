const chatForm = document.querySelector('.chat-form');
const messageInput = document.querySelector('#message');
const sendBtn = document.querySelector('#send-btn');
const chatMessages = document.querySelector('.chat-messages');

sendBtn.addEventListener('click', async (e) => {
	e.preventDefault();
	const message = messageInput.value.trim();
	if (message!== '') {
		await fetch('/send_message', {
			method: 'POST',
			body: new URLSearchParams(new FormData(chatForm)),
		});
		messageInput.value = '';
	}
});

async function getMessages() {
	const response = await fetch('/get_messages');
	const data = await response.json();
	chatMessages.innerHTML = '';
	data.messages.forEach((message) => {
		const messageHTML = `
			<div>
				<p>${message.text}</p>
				<small>${message.user}</small>
			</div>
		`;
		chatMessages.innerHTML += messageHTML;
	});
}

getMessages();
setInterval(getMessages, 1000); // update messages every 1 second