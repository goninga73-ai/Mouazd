let files = JSON.parse(localStorage.getItem("files")) || [];

function login() {
  const pass = document.getElementById("adminPass").value;
  if (pass === "123") {
    document.getElementById("adminPanel").classList.remove("hidden");
  } else {
    alert("كلمة السر غلط 👀");
  }
}

function addFile() {
  const name = document.getElementById("fileName").value;
  const link = document.getElementById("fileLink").value;

  if (!name || !link) {
    alert("عبي كل الحقول");
    return;
  }

  files.push({ name, link });
  localStorage.setItem("files", JSON.stringify(files));
  renderFiles();

  document.getElementById("fileName").value = "";
  document.getElementById("fileLink").value = "";
}

function renderFiles() {
  const list = document.getElementById("filesList");
  list.innerHTML = "";

  files.forEach(file => {
    list.innerHTML += `
      <div class="file">
        <strong>${file.name}</strong><br>
        <a href="${file.link}" download>تحميل</a>
      </div>
    `;
  });
}

renderFiles();