from PIL import Image, ImageTk
import numpy as np
import constants
import subprocess
import os

class ImageProcessor:
    def __init__(self, filename):
        self.img = Image.open(filename).convert('L')
        self.img_org = self.img.resize((390,390))
        self.img_array = np.array (self.img_org)
    
    def get_or_img(self):
        return ImageTk.PhotoImage(self.img_org);

    def process_quadrant(self, quadrantN):
        quadrantArray = self.get_quadrant_array(quadrantN)
        fileName = f"quadrant.img"
        self.save_quadrant(quadrantArray,fileName)
        # 1. Ensamblar .asm a .o
        subprocess.run(["nasm", "-felf64", "-o", "sub_interpolation.o", "sub_interpolation.asm"], check=True)
        # 2. Ligar .o a ejecutable
        subprocess.run(["ld", "-o", "sub_interpolation", "sub_interpolation.o"], check=True)
        # 3. Ejecutar el programa directamente en Linux
        subprocess.run(["./sub_interpolation"], check = True)
        self.img_to_jpeg("output.img", "prueba.jpg", 385, 385)
        #self.pruebita()
    
    def pruebita(self):
        # Configuración
        ancho = 97
        alto = 97

        # Leer archivos
        input_data = np.fromfile('quadrant.img', dtype=np.uint8)
        output_data = np.fromfile('output.img', dtype=np.uint8)

        # Mostrar diferencias en hexadecimal
        N = 100  # mostrar primeros 100 píxeles
        print(f"{'Index':>5} {'Input (hex)':>12} {'Output (hex)':>12} {'Expected Output':>16}")

        for i in range(N):
            original = input_data[i]
            processed = output_data[i]
            expected = (original + 1) & 0xFF
            print(f"{i:5} {original:12X} {processed:12X} {expected:16X}")

        # Validar que todos estén bien
        success = np.all((input_data + 1) & 0xFF == output_data)
        print("\n¿Todos los píxeles son input + 1? ->", "✅ Sí" if success else "❌ No")
        
    def get_quadrant_array(self, quadrantN):
        rowN = (quadrantN - 1) // 4
        colN = (quadrantN - 1) % 4
        startRow = rowN * constants.QUADRANT_SIZE
        startCol = colN * constants.QUADRANT_SIZE
        return self.img_array[startRow:startRow + constants.QUADRANT_SIZE, startCol: startCol + constants.QUADRANT_SIZE]
    
    def save_quadrant(self, quadrantArray,fileName):
        quadrantBytes = quadrantArray.tobytes()
        with open(fileName,'wb') as f:
            f.write(quadrantBytes)

    def img_to_jpeg(self, inputFileName, outputFileName, width, height):
        with open(inputFileName, 'rb') as f:
            data = f.read()
        img_array = np.frombuffer(data, dtype=np.uint8)

        if len(img_array) != width * height:
            raise ValueError(f"El tamaño del archivo no coincide con {width}x{height}")
        
        img_array = img_array = img_array.reshape((height,width))
        img = Image.fromarray(img_array, mode = 'L')
        img.save(outputFileName, format='JPEG')
def contar_bytes(filename):
    try:
        with open(filename, 'rb') as f:
            data = f.read()
            size = len(data)
            print(f"El archivo '{filename}' tiene {size} bytes.")
            return size
    except FileNotFoundError:
        print(f"❌ El archivo '{filename}' no se encontró.")
        return None
def generate_output_file(input_path, output_path):
     """
     Genera un archivo output.img aplicando interpolación bilineal a los datos
     contenidos en input.img.
     
     Args:
         input_path: Ruta del archivo de entrada (por defecto se busca en el directorio de ejecución)
         output_path: Ruta del archivo de salida (por defecto se guarda en el directorio de ejecución)
     
     Returns:
         bool: True si la operación fue exitosa, False en caso contrario
     """
     try:
         # Si no se especifica ruta, usar el directorio actual
         if input_path is None:
             input_path = os.path.join(os.getcwd(), "input.img")
         if output_path is None:
             output_path = os.path.join(os.getcwd(), "output.img")
         
         # Verificar que existe el archivo input.img
         if not os.path.exists(input_path):
             print(f"Error: No se encontró el archivo {input_path}")
             return False
         
         # Abrir el archivo input.img para lectura binaria
         with open(input_path, 'rb') as f_in:
             input_data = f_in.read()
         
         # Verificar que hay datos
         if len(input_data) == 0:
             print("Error: El archivo input.img está vacío")
             return False
         
         # Abrir el archivo output.img para escritura binaria
         with open(output_path, 'wb') as f_out:
             # Procesar datos en bloques de 4 bytes (cuadrantes 2x2)
             for i in range(0, len(input_data), 4):
                 # Si no hay suficientes bytes para un cuadrante completo, salir
                 if i + 3 >= len(input_data):
                     break
                 
                 # Obtener los 4 valores del cuadrante 2x2
                 a = input_data[i]
                 b = input_data[i+1]
                 c = input_data[i+2]
                 d = input_data[i+3]
                 
                 # Calcular valores interpolados horizontales y verticales
                 a1 = int((2/3)*a + (1/3)*b)
                 b1 = int((1/3)*a + (2/3)*b)
                 c1 = int((2/3)*a + (1/3)*c)
                 g1 = int((1/3)*a + (2/3)*c)
                 k1 = int((2/3)*c + (1/3)*d)
                 l1 = int((1/3)*c + (2/3)*d)
                 f1 = int((2/3)*b + (1/3)*d)
                 j1 = int((1/3)*b + (2/3)*d)
                 
                 # Calcular valores interpolados internos
                 d1 = int((2/3)*c1 + (1/3)*f1)
                 e1 = int((1/3)*c1 + (2/3)*f1)
                 h1 = int((2/3)*g1 + (1/3)*j1)
                 i1 = int((1/3)*g1 + (2/3)*j1)
                 
                 # Guardar los 16 valores del cuadrante 4x4 en el archivo de salida
                 f_out.write(bytes([a, a1, b1, b,
                                   c1, d1, e1, f1,
                                   g1, h1, i1, j1,
                                   c, k1, l1, d]))
         
         return True
     
     except Exception as e:
         print(f"Error al generar el archivo output.img: {str(e)}")
         return False