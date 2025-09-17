from flask import Flask, render_template, request, redirect, send_file, jsonify
import sqlite3
import pandas as pd
from io import BytesIO

app = Flask(__name__)
DB = "pacientes.db"

# Crear tabla si no existe
conn = sqlite3.connect(DB)
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS pacientes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    provincia TEXT, municipio TEXT, policlinico TEXT, nombre TEXT,
    sexo TEXT, fecha_nac TEXT, edad INTEGER, grupo_disp TEXT,
    escolaridad TEXT, ocupacion TEXT, color_piel TEXT,
    factor_riesgo TEXT, riesgo_preconcepcional TEXT,
    embarazada TEXT, enfermedades TEXT, discapacidades TEXT,
    lactante TEXT, mujer_fertil TEXT
)
""")
conn.commit()
conn.close()

# ---------- FUNCIONES AUXILIARES ----------
def calcular_lactante_mujer(edad, sexo):
    lactante = "Sí" if edad == 0 else "No"
    mujer_fertil = "Sí" if 15 <= edad <= 49 and sexo == "F" else "No"
    return lactante, mujer_fertil

# ---------- RUTAS ----------
@app.route("/", methods=["GET"])
def index():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT * FROM pacientes")
    pacientes = c.fetchall()
    conn.close()
    return render_template("index.html", pacientes=pacientes)

@app.route("/agregar", methods=["POST"])
def agregar():
    data = request.form.to_dict()
    edad = int(data.get("edad") or 0)
    sexo = data.get("sexo")
    lactante, mujer_fertil = calcular_lactante_mujer(edad, sexo)
    data["lactante"] = lactante
    data["mujer_fertil"] = mujer_fertil

    # Normalizar campos múltiples
    for campo in ["factor_riesgo", "riesgo_preconcepcional", "enfermedades", "discapacidades"]:
        data[campo] = ", ".join([x.strip() for x in data.get(campo, "").split(",") if x.strip()])

    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
        INSERT INTO pacientes (
            provincia, municipio, policlinico, nombre, sexo, fecha_nac, edad,
            grupo_disp, escolaridad, ocupacion, color_piel,
            factor_riesgo, riesgo_preconcepcional, embarazada,
            enfermedades, discapacidades, lactante, mujer_fertil
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, [data["provincia"], data["municipio"], data["policlinico"], data["nombre"],
          data["sexo"], data["fecha_nac"], edad, data["grupo_disp"], data["escolaridad"],
          data["ocupacion"], data["color_piel"], data["factor_riesgo"],
          data["riesgo_preconcepcional"], data["embarazada"], data["enfermedades"],
          data["discapacidades"], data["lactante"], data["mujer_fertil"]])
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("DELETE FROM pacientes WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"status": "ok"})

@app.route("/export")
def export():
    conn = sqlite3.connect(DB)
    df = pd.read_sql_query("SELECT * FROM pacientes", conn)
    conn.close()
    output = BytesIO()
    df.to_excel(output, index=False)
    output.seek(0)
    return send_file(output, download_name="pacientes.xlsx", as_attachment=True)

@app.route("/filtrar", methods=["POST"])
def filtrar():
    criterios = request.json  # dict {campo: valor}
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    query = "SELECT * FROM pacientes WHERE 1=1"
    params = []
    for campo, valor in criterios.items():
        query += f" AND LOWER({campo}) LIKE ?"
        params.append(f"%{valor.lower()}%")
    c.execute(query, params)
    resultados = c.fetchall()
    conn.close()
    return jsonify(resultados)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
