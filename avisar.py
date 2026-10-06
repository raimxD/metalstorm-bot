
import json, os, time, urllib.request

JSON_URL = "https://ilycons.github.io/metalstorm/rotacion.json"
WEBHOOK = os.environ["DISCORD_WEBHOOK"]
HEADERS = {"User-Agent": "MetalstormBot/1.0", "Content-Type": "application/json"}

MODOS = {
    "deathmatch": "Combate a Muerte por Equipos (TDM)",
    "control": "Control",
    "prioritytarget": "Priority Target",
}
MAPAS = {"Canyon": "Cañón carmesí"}
CLIMAS = {"day": "día", "night": "noche", "sunrise": "amanecer", "snow": "nieve"}


def descargar():
    req = urllib.request.Request(JSON_URL, headers=HEADERS)
    return json.load(urllib.request.urlopen(req, timeout=30))


def describir(slot):
    mapa, clima, modo = slot.split(":")
    return f"**{MODOS.get(modo, modo)}** en {MAPAS.get(mapa, mapa)} ({CLIMAS.get(clima, clima)})"


data = descargar()
ref = data["referenceUnixSeconds"]
ciclo = data["cycleSeconds"]
paso = data["slotSeconds"]
slots = data["slots"]


def slot_en(t):
    return slots[((t - ref) % ciclo) // paso]


ahora = int(time.time())
inicio = ahora - ((ahora - ref) % paso)
fin = inicio + paso

texto = f"🛩️ **Ahora:** {describir(slot_en(ahora))}\n"
texto += f"⏳ Cambia <t:{fin}:R> (a las <t:{fin}:t>)\n\n**Próximos modos:**\n"
for i in range(1, 4):
    t = inicio + i * paso
    texto += f"• <t:{t}:t> — {describir(slot_en(t))}\n"

cuerpo = json.dumps({"content": texto, "username": "Metalstorm Rotación"}).encode()
req = urllib.request.Request(WEBHOOK, data=cuerpo, headers=HEADERS, method="POST")
urllib.request.urlopen(req, timeout=30)
print("Mensaje enviado")
