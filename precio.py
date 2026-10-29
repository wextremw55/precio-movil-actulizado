import csv, datetime, os, sys, requests

SKU = "SVIVX300P16512DMLIBA"
URL = f"https://wss2.cex.es.webuy.io/v3/boxes/{SKU}/detail"
ARCHIVO = "precios.csv"

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
    w.writerow([datetime.date.today().isoformat(), nombre, precio, sin_stock])

print(nombre, precio, "EUR")
