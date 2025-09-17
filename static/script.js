// ------------------ ELIMINAR PACIENTE ------------------
function eliminarPaciente(id) {
  if (confirm("¿Eliminar paciente seleccionado?")) {
    fetch(`/eliminar/${id}`, { method: "POST" })
      .then(res => res.json())
      .then(data => {
        if (data.status == "ok") location.reload();
      });
  }
}

// ------------------ BÚSQUEDA RÁPIDA ------------------
const input = document.getElementById("searchInput");
input.addEventListener("input", function () {
  const texto = this.value.toLowerCase();
  const tabla = document.getElementById("tablaPacientes");
  for (let i = 1; i < tabla.rows.length; i++) {
    let row = tabla.rows[i];
    let mostrar = false;
    for (let j = 1; j < row.cells.length; j++) { // saltamos columna Acciones
      let cell = row.cells[j];
      cell.innerHTML = cell.textContent; // reset highlight
      if (cell.textContent.toLowerCase().includes(texto) && texto != "") {
        mostrar = true;
        let re = new RegExp(texto, "gi");
        cell.innerHTML = cell.textContent.replace(
          re,
          match => `<span class="highlight">${match}</span>`
        );
      }
    }
    row.style.display = mostrar || texto == "" ? "" : "none";
  }
});

// ------------------ FILTRO AVANZADO ------------------
function abrirFiltro() {
  document.getElementById("modalFiltro").style.display = "block";
  document.getElementById("overlay").style.display = "block";
}

function cerrarFiltro() {
  document.getElementById("modalFiltro").style.display = "none";
  document.getElementById("overlay").style.display = "none";
}

// ------------------ APLICAR FILTRO ------------------
function aplicarFiltro() {
  const form = document.getElementById("formFiltro");
  const criterios = {};

  // Recorremos inputs y añadimos solo los que tienen valor
  for (let i = 0; i < form.elements.length; i++) {
    let el = form.elements[i];
    if (el.tagName === "INPUT" && el.value.trim() !== "") {
      criterios[el.name] = el.value.trim();
    }
  }

  fetch("/filtrar", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(criterios)
  })
    .then(res => res.json())
    .then(data => {
      const tabla = document.getElementById("tablaPacientes");
      tabla.tBodies[0].innerHTML = "";
      data.forEach(p => {
        let tr = document.createElement("tr");
        tr.innerHTML =
          `<td><button onclick="eliminarPaciente(${p[0]})">Eliminar</button></td>` +
          p.slice(1).map(v => `<td>${v}</td>`).join("");
        tabla.tBodies[0].appendChild(tr);
      });
      cerrarFiltro();
    });
}
