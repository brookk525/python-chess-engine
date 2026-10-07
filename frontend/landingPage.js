const $ = (id) => document.getElementById(id);

async function onPlayClick() {
    const name = $("username")?.value?.trim();

    if (!name) {
        alert("Mete tu nombre primero.");
        return;
    }

    try {
        const res = await fetch("/api/register", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name })
        });

        const data = await res.json();

        if (!res.ok || !data.succeded) {
            alert(data.name || "Error registrando.");
            return;
        }

        localStorage.setItem("username", data.name);
        window.location.href = "/frontend/usermenu.html";
    } catch {
        alert("Error de red.");
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const btn = $("register"); // tu botón PLAY tiene id="register"
    if (btn) btn.addEventListener("click", onPlayClick);
});