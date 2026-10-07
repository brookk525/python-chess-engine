const username = localStorage.getItem("username") || "Jugador";
document.getElementById("usernameLabel").textContent = username;

document.getElementById("playBtn").addEventListener("click", () => {
    window.location.href = "/frontend/lista.html";
});