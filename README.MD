# Proyecto de Interpolación Bilineal en Ensamblador

**Autor:** Daniel Duarte Cordero

## Descripción del Proyecto

Este proyecto implementa la interpolación bilineal de un cuadrante de una imagen utilizando lenguaje ensamblador sobre arquitectura x86-64. La imagen de entrada se convierte a escala de grises, se divide en cuadrantes, y se procesa para obtener una imagen interpolada de mayor resolución. La visualización y automatización del flujo de trabajo se realiza mediante un programa desarrollado en Python.

## Herramientas utilizadas

- **Visual Studio Code**: Editor de código para el desarrollo de scripts en Python y archivos en ensamblador.
- **NASM**: Ensamblador utilizado para generar archivos objeto (`.o`) a partir del código en lenguaje ensamblador.
- **LD**: Enlazador de GNU utilizado para generar ejecutables a partir de los archivos objeto.
- **GDB**: Depurador utilizado para el análisis y depuración del programa ensamblador.
- **Python** (con librerías `Pillow`, `NumPy`, `Tkinter`): Para la conversión de imágenes, selección de cuadrantes, automatización de ejecución y visualización de resultados.

## Instrucciones de uso

1. Asegurarse de tener instaladas las siguientes herramientas en el sistema:
   - `nasm`
   - `ld`
   - `gdb` (opcional, para depuración)
   - Python 3 (con las librerías `Pillow`, `NumPy`, `Tkinter`)

2. Ejecutar el programa en Python (`GUI.py`) para cargar la imagen de entrada (`entrada.jpg`).

3. En la interfaz gráfica:
   - Seleccionar el número de cuadrante (1–16) a procesar.
   - Presionar el botón **Interpolar**.

4. El programa realizará automáticamente:
   - La conversión del cuadrante seleccionado a formato `.img`.
   - El ensamblaje (`nasm -felf64 interpolation.asm`) y enlace (`ld -o interpolation interpolation.o`) del código en ensamblador.
   - La ejecución del programa ensamblador (`./interpolation`) para generar el archivo `output.img` interpolado.

5. Visualizar los resultados:
   - La imagen del cuadrante seleccionado sin interpolar.
   - La imagen del cuadrante interpolado resultante.

## Estructura de archivos principales

- `interpolation.asm`: Código fuente en lenguaje ensamblador para realizar la interpolación bilineal.
- `GUI.py`: Programa en Python para la carga de imagen, selección de cuadrantes y visualización de resultados.
- `entrada.jpg`: Imagen original en formato JPEG utilizada como entrada.
- `quadrant.img`: Archivo binario de imagen correspondiente al cuadrante seleccionado.
- `output.img`: Archivo binario generado por el programa en ensamblador, correspondiente a la imagen interpolada.

---
