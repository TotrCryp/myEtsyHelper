async function loadUsers() {
  const res = await fetch("http://127.0.0.1:8000/ads-keywords/");
  const users = await res.json();
  const list = document.getElementById("users");
  list.innerHTML = "";
  users.forEach(u => {
    const li = document.createElement("li");
    li.textContent = `${u.id}: ${u.name} (${u.email})`;
    list.appendChild(li);
  });
}

async function addUser() {
  const keyword = document.getElementById("name").value;
//  const email = document.getElementById("email").value;
  await fetch("http://127.0.0.1:8000/ads-keywords/", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({keyword,})
  });
  loadUsers();
}

loadUsers();
