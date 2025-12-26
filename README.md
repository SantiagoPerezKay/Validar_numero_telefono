# Normalizador y Validador de Números Telefónicos (Argentina)

Script en **Python** para limpiar, normalizar y validar números telefónicos argentinos a partir de un archivo **CSV**.

Convierte números escritos en cualquier formato a un formato estándar tipo **E.164** para Argentina:

+54XXXXXXXXXX
+549XXXXXXXXXX

yaml
Copiar código

Ideal para:
- Listas de WhatsApp
- Campañas de marketing
- CRMs
- Limpieza de bases de datos

---

## 🚀 Qué hace

- Lee un archivo **CSV**
- Toma el **primer valor de cada fila**
- Elimina caracteres inválidos
- Normaliza números argentinos
- Valida formato final
- Descarta números incorrectos
- Imprime resultados en bloques de **50 números**

---

## 📥 Formato de entrada

Archivo CSV simple, por ejemplo:

```csv
3462-516761
+54 11 1234-5678
(3462) 516761
9 3462 516761
texto inválido
Solo se procesa la primera columna de cada fila.

📤 Formato de salida
Ejemplo de salida en consola:

text
Copiar código
+543462516761,+541112345678,+5493462516761
--------------------------------------
+543411223344,+5491122334455
Y al final:

text
Copiar código
Total de números válidos procesados: 42
🧠 Reglas de normalización
El script soporta y corrige formatos como:

Entrada	Salida
3462516761	+543462516761
93462516761	+5493462516761
543462516761	+543462516761
+5493462516761	+5493462516761

✅ Validación aplicada
Se consideran válidos los números que cumplan:

Empiecen con +54

Tengan 12 o 13 dígitos en total

Coincidan con el patrón:

regex
Copiar código
^\+54\d{10,11}$
Todo lo que no cumpla esto se descarta.

▶️ Uso
Requisitos
Python 3.7+

No requiere librerías externas

Ejecutar
bash
Copiar código
python limpiar_numeros.py
El script va a pedir:

text
Copiar código
Ingresa la ruta del archivo CSV:
Pegás la ruta y listo.

🧪 Opcional: guardar resultado en archivo
En el código está preparado para exportar el resultado:

python
Copiar código
with open("salida_numeros.txt", "w") as f:
    f.write(resultado)
Solo tenés que descomentar esas líneas.

⚠️ Consideraciones
No valida si el número existe

Solo valida formato

No distingue móviles vs fijos

Procesa solo Argentina (+54)
