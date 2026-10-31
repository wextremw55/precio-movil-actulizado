import csv, datetime, os, sys, requests

SKU = "SVIVX300P16512DMLIBA"
URL = f"https://wss2.cex.es.webuy.io/v3/boxes/{SKU}/detail"
ARCHIVO = "precios.csv"
hoy = datetime.date.today().isoformat()

if os.path.exists(ARCHIVO):
    with open(ARCHIVO, encoding="utf-8") as f:
        if any(linea.startswith(hoy) for linea in f):
            print("Ya hay un precio de hoy")
            sys.exit(0)

r = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
r.raise_for_status()
caja = r.json()["response"]["data"]["boxDetails"][0]

nombre = caja.get("boxName", "")
precio = caja.get("sellPrice")
sin_stock = caja.get("outOfStock", 0)

if precio is None:
    sys.exit("No se encontró el precio en la respuesta")

nuevo = not os.path.exists(ARCHIVO)
with open(ARCHIVO, "a", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    if nuevo:
        w.writerow(["fecha", "producto", "precio_eur", "sin_stock"])
    w.writerow([hoy, nombre, precio, sin_stock])

print(nombre, precio, "EUR")
