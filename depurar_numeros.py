import csv
import re

def validar_numero_completo(num_limpio):
    """
    Valida si un número limpio cumple con el formato estándar argentino:
    +54(código de área)(número), con un total de 12 o 13 dígitos después del +
    Ejemplos válidos: +543462516761, +541112345678
    """
    # El patrón busca:
    # ^\+54 : Comienza con +54
    # \d{10,11}$ : Seguido de 10 u 11 dígitos hasta el final de la cadena.
    # El 9 inicial del código de área se elimina en la normalización, así que
    # un número de 10 dígitos (ej. 3462 516761) se convierte a +543462516761 (12 digitos en total)
    # y un número de 11 dígitos (ej. 11 12345678) a +541112345678 (12 digitos en total)
    # Algunos números pueden ser más largos, como +54911... que tiene 13 dígitos.
    # Es una validación flexible para capturar la mayoría de los casos.
    if re.match(r'^\+54\d{10,11}$', num_limpio):
        return True
    return False

def limpiar_numero(num):
    # Quitar todo excepto dígitos
    solo_digitos = re.sub(r'\D', '', num)

    if len(solo_digitos) == 0:
        return ""

    # Normalización del número
    if solo_digitos.startswith("549"):
        # Ejemplo: 5493462516761 -> +5493462516761 (13 dígitos)
        num_normalizado = "+" + solo_digitos
    elif solo_digitos.startswith("54"):
        # Ejemplo: 543462516761 -> +543462516761 (12 dígitos)
        num_normalizado = "+" + solo_digitos
    elif solo_digitos.startswith("9"):
        # Ejemplo: 93462516761 -> +5493462516761 (13 dígitos)
        num_normalizado = "+54" + solo_digitos
    else:
        # Si empieza con otro número, agregar +54 (sin el 9)
        # Ejemplo: 3462516761 -> +543462516761 (12 dígitos)
        num_normalizado = "+54" + solo_digitos
    
    # Validar el número normalizado
    if validar_numero_completo(num_normalizado):
        return num_normalizado
    else:
        # Si no cumple el formato, ignorarlo devolviendo una cadena vacía
        return ""

def procesar_csv(ruta):
    numeros_limpios = []

    try:
        with open(ruta, newline='', encoding='utf-8') as csvfile:
            lector = csv.reader(csvfile)
            for fila in lector:
                if len(fila) == 0:
                    continue
                num_original = fila[0]
                num_limpio = limpiar_numero(num_original)
                # Solo agrega el número si no está vacío (es decir, si la validación fue exitosa)
                if num_limpio:
                    numeros_limpios.append(num_limpio)
    except FileNotFoundError:
        raise
    except Exception as e:
        print(f"Error al procesar el archivo: {e}")
        return []

    return numeros_limpios

def imprimir_numeros_con_saltos(numeros):
    """
    Imprime los números con saltos de línea cada 50 números válidos
    """
    print("\nNúmeros depurados y formateados:")
    
    count = 0
    linea_actual = []
    
    for numero in numeros:
        linea_actual.append(numero)
        count += 1
        
        # Cada 50 números, imprimir la línea y hacer un salto
        if count == 50:
            print(",".join(linea_actual))
            print("--------------------------------------")
            linea_actual = []
            count = 0
    
    # Imprimir los números restantes si los hay
    if linea_actual:
        print(",".join(linea_actual))

def main():
    ruta = input("Ingresa la ruta del archivo CSV: ").strip()
    try:
        numeros = procesar_csv(ruta)
        
        if numeros:
            # Imprimir con saltos cada 50 números
            imprimir_numeros_con_saltos(numeros)
            
            print(f"\nTotal de números válidos procesados: {len(numeros)}")
            
            # Opcional: Escribir la salida a un archivo
            # resultado = ",".join(numeros)
            # with open("salida_numeros.txt", "w") as f:
            #     f.write(resultado)
            #     print("\nResultado guardado en 'salida_numeros.txt'")
        else:
            print("No se encontraron números válidos en el archivo.")
            
    except FileNotFoundError:
        print("Archivo no encontrado. Por favor verifica la ruta.")
    except Exception as e:
        print("Ocurrió un error:", e)

if __name__ == "__main__":
    main()