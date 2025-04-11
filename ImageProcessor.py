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
        subprocess.run(["nasm", "-felf64", "-o", "interpolation.o", "interpolation.asm"], check=True)
        # 2. Ligar .o a ejecutable
        subprocess.run(["ld", "-o", "interpolation", "interpolation.o"], check=True)
        # 3. Ejecutar el programa directamente en Linux
        subprocess.run(["./interpolation"], check = True)
        self.img_to_jpeg("output.img", "interpolada.jpg", 385, 385)
        self.img_to_jpeg(fileName, "no_interpolada.jpg", 97, 97)
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
