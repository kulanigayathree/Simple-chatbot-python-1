document.getElementById("chat-form").addEventListener("submit", async function (e) {
  e.preventDefault();
  const inputBox = document.getElementById("user-input");
  const chatBox = document.getElementById("chat-box");
  const userText = inputBox.value;

  const userDiv = document.createElement("div");
  userDiv.className = "user-message";
  userDiv.textContent = userText;
  chatBox.appendChild(userDiv);

  const res = await fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: userText })
  });
  const data = await res.json();

  const botDiv = document.createElement("div");
  botDiv.className = "bot-message";
  botDiv.textContent = data.response;
  chatBox.appendChild(botDiv);

  inputBox.value = "";
  chatBox.scrollTop = chatBox.scrollHeight;
});
