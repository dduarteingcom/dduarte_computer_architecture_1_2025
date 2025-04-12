from PIL import Image, ImageTk
import numpy as np
import constants
import subprocess

class ImageProcessor:
    """
    Clase que gestiona la carga, segmentación, procesamiento y visualización de imágenes
    para interpolación bilineal, en el contexto del proyecto de Arquitectura de Computadores I.
    """

    def __init__(self, filename):
        """
        Constructor de la clase.
        
        Parámetros:
        filename (str): Ruta del archivo de imagen a procesar.
        """
        # Cargar la imagen en escala de grises ('L' = luminancia)
        self.img = Image.open(filename).convert('L')
        # Redimensionar la imagen a 390x390 píxeles
        self.img_org = self.img.resize((390, 390))
        # Convertir la imagen a un arreglo de numpy para manipulación de píxeles
        self.img_array = np.array(self.img_org)
    
    def get_or_img(self):
        """
        Devuelve la imagen original redimensionada como un objeto compatible con Tkinter.

        Retorna:
        ImageTk.PhotoImage: Imagen lista para ser mostrada en una GUI.
        """
        return ImageTk.PhotoImage(self.img_org)

    def process_quadrant(self, quadrantN):
        """
        Procesa el cuadrante especificado: lo guarda, ensambla, ejecuta el programa
        en ensamblador y genera las imágenes resultantes.
        
        Parámetros:
        quadrantN (int): Número de cuadrante a procesar (1–16).
        """
        # Extraer el arreglo correspondiente al cuadrante seleccionado
        quadrantArray = self.get_quadrant_array(quadrantN)
        fileName = f"quadrant.img"
        
        # Guardar el cuadrante como archivo binario .img
        self.save_quadrant(quadrantArray, fileName)
        
        # Ensamblar el código en NASM (interpolation.asm -> interpolation.o)
        subprocess.run(["nasm", "-felf64", "-o", "interpolation.o", "interpolation.asm"], check=True)
        
        # Ligar el objeto ensamblado a un ejecutable (interpolation.o -> interpolation)
        subprocess.run(["ld", "-o", "interpolation", "interpolation.o"], check=True)
        
        # Ejecutar el programa en ensamblador (interpolación bilineal)
        subprocess.run(["./interpolation"], check=True)
        
        # Convertir archivo de salida interpolado a imagen JPEG de 385x385 píxeles
        self.img_to_jpeg("output.img", "interpolada.jpg", 385, 385)
        
        # Convertir el cuadrante sin interpolar a imagen JPEG de 97x97 píxeles
        self.img_to_jpeg(fileName, "no_interpolada.jpg", 97, 97)
        
    def get_quadrant_array(self, quadrantN):
        """
        Obtiene el arreglo de píxeles correspondiente a un cuadrante específico de la imagen.
        
        Parámetros:
        quadrantN (int): Número de cuadrante (1–16).

        Retorna:
        numpy.ndarray: Submatriz del cuadrante seleccionado.
        """
        # Determinar fila y columna del cuadrante basado en un grid de 4x4
        rowN = (quadrantN - 1) // 4
        colN = (quadrantN - 1) % 4
        
        # Calcular las coordenadas de inicio
        startRow = rowN * constants.QUADRANT_SIZE
        startCol = colN * constants.QUADRANT_SIZE
        
        # Devolver la submatriz 97x97 correspondiente al cuadrante
        return self.img_array[startRow:startRow + constants.QUADRANT_SIZE,
                              startCol: startCol + constants.QUADRANT_SIZE]
    
    def save_quadrant(self, quadrantArray, fileName):
        """
        Guarda un arreglo de imagen como archivo binario (.img).
        
        Parámetros:
        quadrantArray (numpy.ndarray): Arreglo de píxeles del cuadrante.
        fileName (str): Nombre del archivo de salida.
        """
        # Convertir el arreglo en una secuencia de bytes
        quadrantBytes = quadrantArray.tobytes()
        
        # Escribir los bytes en el archivo .img
        with open(fileName, 'wb') as f:
            f.write(quadrantBytes)

    def img_to_jpeg(self, inputFileName, outputFileName, width, height):
        """
        Convierte un archivo .img (formato binario) en una imagen JPEG de escala de grises.
        
        Parámetros:
        inputFileName (str): Nombre del archivo binario de entrada (.img).
        outputFileName (str): Nombre del archivo de imagen de salida (.jpg).
        width (int): Ancho esperado de la imagen.
        height (int): Altura esperada de la imagen.
        """
        # Leer los datos binarios
        with open(inputFileName, 'rb') as f:
            data = f.read()
        
        # Convertir los datos binarios en un arreglo de numpy
        img_array = np.frombuffer(data, dtype=np.uint8)

        # Verificar que el tamaño del archivo sea consistente
        if len(img_array) != width * height:
            raise ValueError(f"El tamaño del archivo no coincide con {width}x{height}")
        
        # Dar forma al arreglo de acuerdo a las dimensiones especificadas
        img_array = img_array.reshape((height, width))
        
        # Crear una imagen PIL desde el arreglo
        img = Image.fromarray(img_array, mode='L')
        
        # Guardar como imagen JPEG
        img.save(outputFileName, format='JPEG')
