import csv, datetime, os, sys, requests

PRODUCTOS = [
    {"sku": "SVIVX300P16512DMLIBA", "archivo": "precios.csv"},
    {"sku": "SOPCPH279712512GLIBA", "archivo": "precios_movil2.csv"},
    {"sku": "SOPPFX9P16512TCLIBA", "archivo": "precios_movil3.csv"},
]

hoy = datetime.date.today().isoformat()
errores = 0

def registrar(sku, archivo):
    if os.path.exists(archivo):
        with open(archivo, encoding="utf-8") as f:
            if any(l.startswith(hoy) for l in f):
                print(f"{archivo}: ya hay precio de hoy")
                return
    url = f"https://wss2.cex.es.webuy.io/v3/boxes/{sku}/detail"
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
    r.raise_for_status()
    caja = r.json()["response"]["data"]["boxDetails"][0]
    precio = caja.get("sellPrice")
    if precio is None:
        raise ValueError("sin precio en la respuesta")
    nuevo = not os.path.exists(archivo)
    with open(archivo, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if nuevo:
            w.writerow(["fecha", "producto", "precio_eur", "sin_stock"])
        w.writerow([hoy, caja.get("boxName", ""), precio, caja.get("outOfStock", 0)])
    print(archivo, precio, "EUR")

for p in PRODUCTOS:
    try:
        registrar(p["sku"], p["archivo"])
    except Exception as e:
        errores += 1
        print(f"Error con {p['sku']}: {e}")

sys.exit(1 if errores else 0)
