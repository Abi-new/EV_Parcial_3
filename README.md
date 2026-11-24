# EV Parcial 3 · CUY6142 · Abiatar Ramirez

Evaluación Parcial N° 3 (Experiencia 3) de **CUY6142 – Telepresencia y Entornos Innovadores de Colaboración Humana**, Duoc UC. Prototipo del canal de atención de TeleAndes con Webex.

Basado en el repositorio oficial del curso: https://github.com/nicsanchezr/cuy6142-exp3

| Carpeta | Contenido |
|---|---|
| `lab2/ep3_abiatar_ramirez.py` | Ítems 1, 2 y 3: crea la sala `abiatar_ramirez` (GET/POST /rooms), agrega al compañero(a) y lista los miembros (POST/GET /memberships) y envía el saludo con emoji e imagen (POST /messages). Usa `webex_utils.py`. |
| `lab3/01_bot_basico.py` | Ítem 4: bot `bot_abiatar_ramirez`, responde a `hola`. |
| `lab3/CUY6142_bot_abiatar_ramirez.postman_collection.json` | Ítem 5: colección de Postman (Parte 5: mensaje al bot con el token personal). |
| `lab3/02_bot_ia.py` y `lab3/ia.py` | Ítem 6: IA con OpenRouter, personalidad **AndesBot** (ejecutivo virtual de TeleAndes) y comando `traducir <idioma>: <texto>`. |

## Ejecución (VM DEVASC)

```bash
# Ítems 1, 2 y 3
cd lab2
cp .env.ejemplo .env      # completar WEBEX_TOKEN, MI_NOMBRE, NOMBRE_COMPLETO, EMAIL_COMPANERO
python3 ep3_abiatar_ramirez.py

# Ítems 4 y 6
cd ../lab3
cp .env.ejemplo .env      # completar WEBEX_BOT_TOKEN, USUARIOS_PERMITIDOS, OPENROUTER_API_KEY
python3.12 -m venv .venv && .venv/bin/pip install -r requirements.txt
source .venv/bin/activate
python 01_bot_basico.py   # ítem 4
python 02_bot_ia.py       # ítem 6
```

Los tokens se guardan solo en los archivos `.env`, que están excluidos por `.gitignore`.
