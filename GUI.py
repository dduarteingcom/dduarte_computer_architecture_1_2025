import tkinter as tk
import constants
from ImageProcessor import ImageProcessor

class GUI: 
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Interpolación")
        #Get Image
        self.processor = ImageProcessor('entrada.jpg')
        self.tk_img = self.processor.get_or_img()

        # Frame de arriba para las imágenes
        self.top_frame = tk.Frame(self.root)
        self.top_frame.pack(side='top', pady=10)


        # Frame izquierdo para Imagen Original
        self.left_frame = tk.Frame(self.top_frame)
        self.left_frame.pack(side='left', padx=10, pady=10)

        #Label Original Image
        self.label1 = tk.Label(
            self.left_frame,
            text= 'Imagen Original',
            font= ("Arial", 16),
            width= constants.IMG_WIDTH//10,
            anchor= 'center',
            pady=10
        
        )
        self.label1.pack()
        
        #Show Image
        self.canvas = tk.Canvas(self.left_frame, width= constants.IMG_WIDTH, height= constants.IMG_HEIGHT)
        self.canvas.pack()
        self.canvas.create_image(0,0, anchor = 'nw', image = self.tk_img)

        #Draw quadrants
        for i in range (1, constants.N_QUADRANTS):
            x = i * constants.QUADRANT_SIZE
            y = x
            self.canvas.create_line(x, 0, x, constants.IMG_HEIGHT, fill='red', width=2)
            self.canvas.create_line(0 ,y ,constants.IMG_WIDTH,y, fill= 'red', width= 2)

        # Frame derecho para Imagen Interpolada
        self.right_frame = tk.Frame(self.top_frame)
        self.right_frame.pack(side='left', padx=10, pady=10)


        #Label Resultant Quadrant
        self.label2 = tk.Label(
            self.right_frame,
            text= 'Cuadrante interpolado',
            font= ("Arial", 16),
            width= 193//10,
            anchor= 'center',
            pady=10
        
        )
        self.label2.pack()
        # Canvas Resultant Quadrant
        self.canvas_interpolated = tk.Canvas(self.right_frame, width=193, height=constants.IMG_HEIGHT)
        self.canvas_interpolated.pack()
        
       # Ahora debajo de las imágenes, frame para controles
        self.bottom_frame = tk.Frame(self.root)
        self.bottom_frame.pack(side='top', pady=20)

        # Label para indicar al usuario
        self.label_entry = tk.Label(self.bottom_frame, text="Número de cuadrante:")
        self.label_entry.pack(side='left', padx=5)

        # Entry para que el usuario escriba el número
        self.quadrant_entry = tk.Entry(self.bottom_frame, width=5)
        self.quadrant_entry.pack(side='left', padx=5)

        # Botón para interpolar
        self.interpolate_button = tk.Button(self.bottom_frame, text="Interpolar", command=self.interpolate_quadrant)
        self.interpolate_button.pack(side='left', padx=5)       

    def show(self):
        self.root.mainloop()

    def interpolate_quadrant(self):
            try:
                quadrant_number = int(self.quadrant_entry.get())
                if 1 <= quadrant_number <= 16:
                    print(f"Interpolando cuadrante {quadrant_number}...")
                    self.processor.process_quadrant(quadrant_number)
                else:
                    print("Número de cuadrante inválido. Debe ser entre 1 y 16.")
            except ValueError:
                print("Por favor ingrese un número válido.")
                        


        