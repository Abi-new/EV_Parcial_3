"""
ep3_abiatar_ramirez.py
Evaluación Parcial N° 3 - CUY6142 - Abiatar Ramirez

Prototipo del canal de atención de TeleAndes con la API REST de Webex.
El script hace tres tareas en orden:
  1. Crear la sala abiatar_ramirez     -> GET /rooms y POST /rooms
  2. Agregar a mi compañero(a)          -> POST /memberships y GET /memberships
  3. Enviar un mensaje con emoji+imagen -> POST /messages

Reutiliza las funciones de webex_utils.py (lectura del token desde .env,
encabezado Authorization: Bearer y manejo de errores HTTP).
Ejecución:  cd ~/labs/cuy6142-exp3/lab2 && python3 ep3_abiatar_ramirez.py
"""
import mimetypes
import os

from webex_utils import cargar_token, cargar_variable, llamar_api, guardar_sala

token = cargar_token()
titulo = cargar_variable("MI_NOMBRE")              # abiatar_ramirez
nombre = cargar_variable("NOMBRE_COMPLETO")        # Abiatar Ramirez
email_companero = cargar_variable("EMAIL_COMPANERO")
IMAGEN = "imagen_prueba.png"


def linea(titulo_paso):
    print("\n" + "=" * 60)
    print(titulo_paso)
    print("=" * 60)


# ---------------------------------------------------------------------------
# Ítem 1: crear la sala (o reutilizarla si ya existe)
# ---------------------------------------------------------------------------
linea("ÍTEM 1 - Crear la sala '{}'".format(titulo))

salas = llamar_api("GET", "rooms", token,
                   params={"type": "group", "max": 100}).json()["items"]
existentes = [sala for sala in salas if sala["title"] == titulo]

if existentes:
    sala = existentes[0]
    print("[OK] GET /rooms: la sala ya existía, se reutiliza.")
else:
    respuesta = llamar_api("POST", "rooms", token, json={"title": titulo})
    sala = respuesta.json()
    print("[OK] POST /rooms: sala creada (HTTP {}).".format(respuesta.status_code))

room_id = sala["id"]
guardar_sala(room_id)
print("     Título de la sala: {}".format(sala["title"]))
print("     ID de la sala    : {}...".format(room_id[:25]))

# ---------------------------------------------------------------------------
# Ítem 2: agregar a mi compañero(a) y listar los miembros
# ---------------------------------------------------------------------------
linea("ÍTEM 2 - Agregar a mi compañero(a) a la sala")

respuesta = llamar_api("POST", "memberships", token, permitir=(409,),
                       json={"roomId": room_id, "personEmail": email_companero})
if respuesta.status_code == 409:
    print("[OK] POST /memberships: {} ya era miembro (HTTP 409).".format(email_companero))
else:
    print("[OK] POST /memberships: {} agregado(a) (HTTP {}).".format(
        email_companero, respuesta.status_code))

miembros = llamar_api("GET", "memberships", token,
                      params={"roomId": room_id}).json()["items"]
print("\n[OK] GET /memberships: la sala tiene {} miembro(s):".format(len(miembros)))
for miembro in miembros:
    rol = "moderador" if miembro.get("isModerator") else "miembro"
    print("  - {:<22} {:<38} {}".format(
        miembro.get("personDisplayName", ""), miembro["personEmail"], rol))

# ---------------------------------------------------------------------------
# Ítem 3: enviar el mensaje de saludo con un emoji y una imagen adjunta
# ---------------------------------------------------------------------------
linea("ÍTEM 3 - Enviar el mensaje a la sala")

texto = "Saludos Webex, mi nombre es {} \U0001F44B".format(nombre)
tipo = mimetypes.guess_type(IMAGEN)[0] or "application/octet-stream"
with open(IMAGEN, "rb") as imagen:
    respuesta = llamar_api(
        "POST", "messages", token,
        data={"roomId": room_id, "text": texto},
        files={"files": (os.path.basename(IMAGEN), imagen, tipo)},
    )

mensaje = respuesta.json()
print("[OK] POST /messages: mensaje publicado (HTTP {}).".format(respuesta.status_code))
print("     Texto   : {}".format(mensaje.get("text", texto)))
print("     Adjuntos: {} ({})".format(len(mensaje.get("files", [])), IMAGEN))
print("     Creado  : {}".format(mensaje.get("created", "")))
print("\nListo: sala, miembros y mensaje creados con la API REST de Webex.")
