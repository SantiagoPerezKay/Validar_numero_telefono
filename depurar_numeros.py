import csv
import re
import os

CARACTERISTICA_DEFAULT = "3462"  # Venado Tuerto
ARCHIVO_SALIDA = "Numeros_clientes_procesados.txt"

def validar_numero_completo(num):
    return re.match(r'^\+54\d{10,13}$', num) is not None

def limpiar_numero(num):
    if not num:
        return ""

    num = num.strip().upper()

    if num in ("ND", "N/D", "NO TIENE", "SIN TELEFONO"):
        return ""

    solo = re.sub(r'\D', '', num)

    if len(solo) < 6:
        return ""

    # Local sin característica (ej: 427357)
    if len(solo) in (6, 7, 8):
        solo = CARACTERISTICA_DEFAULT + solo

    # Celular con 15 (ej: 346215427357)
    if len(solo) == 12 and solo[4:6] == "15":
        solo = solo[:4] + solo[6:]

    # Sin país
    if not solo.startswith("54"):
        solo = "54" + solo

    num_final = "+" + solo

    return num_final if validar_numero_completo(num_final) else ""
def procesar_csv(ruta):
    numeros_limpios = []      # mantiene orden
    vistos = set()            # evita duplicados

    encodings = ["utf-8", "latin-1", "cp1252"]

    for enc in encodings:
        try:
            with open(ruta, newline='', encoding=enc) as csvfile:
                lector = csv.reader(csvfile)
                for fila in lector:
                    if not fila:
                        continue

                    num_limpio = limpiar_numero(fila[0])

                    if num_limpio and num_limpio not in vistos:
                        numeros_limpios.append(num_limpio)
                        vistos.add(num_limpio)

            print(f"Archivo leído correctamente con encoding: {enc}")
            break

        except UnicodeDecodeError:
            continue

    else:
        raise Exception("No se pudo leer el archivo con UTF-8 ni Latin-1")

    return numeros_limpios



def guardar_numeros(numeros):
    if not numeros:
        return

    with open(ARCHIVO_SALIDA, "a", encoding="utf-8") as f:
        f.write(",".join(numeros) + ",")

def imprimir_numeros_con_saltos(numeros):
    print("\nNúmeros depurados y formateados:")

    for i in range(0, len(numeros), 50):
        print(",".join(numeros[i:i+50]))
        print("--------------------------------------")

def main():
    ruta = input("Ingresa la ruta del archivo CSV: ").strip()

    try:
        numeros = procesar_csv(ruta)

        if not numeros:
            print("No se encontraron números válidos.")
            return

        imprimir_numeros_con_saltos(numeros)
        guardar_numeros(numeros)

        print(f"\nTotal de números válidos procesados: {len(numeros)}")
        print(f"Archivo actualizado: {ARCHIVO_SALIDA}")

    except FileNotFoundError:
        print("Archivo no encontrado.")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
