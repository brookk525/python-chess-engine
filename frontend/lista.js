const $ = (id) => document.getElementById(id);

function clearView() {
    $("usersList").innerHTML = "";
    $("status").textContent = "";
}

async function loadUsers() {
    $("status").textContent = "Cargando...";
    $("usersList").innerHTML = "";

    try {
        const res = await fetch("/api/users");
        const data = await res.json();

        if (!res.ok) {
            $("status").textContent = "Error HTTP " + res.status;
            return;
        }

        const users = data.users || [];

        if (users.length === 0) {
            $("status").textContent = "No hay usuarios todavía.";
            return;
        }

        $("status").textContent = `Usuarios: ${users.length}`;

        users.forEach((u, i) => {
            const li = document.createElement("li");
            li.innerHTML = `<span>${u}</span><span class="badge">#${i + 1}</span>`;
            $("usersList").appendChild(li);
        });

    } catch (e) {
        $("status").textContent = "Error de red.";
    }
}

document.addEventListener("DOMContentLoaded", () => {
    $("loadBtn").addEventListener("click", loadUsers);
    $("clearViewBtn").addEventListener("click", clearView);

    // Auto-cargar al entrar (opcional). Si no lo quieres, borra esta línea:
    loadUsers();
});