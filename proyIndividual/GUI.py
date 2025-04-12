import tkinter as tk
import constants
from ImageProcessor import ImageProcessor
from PIL import Image, ImageTk

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

        # Opcional: Configurar el espaciado entre columnas del grid
        self.top_frame.grid_columnconfigure(0, weight=1, pad=0)
        self.top_frame.grid_columnconfigure(1, weight=1, pad=0)
        self.top_frame.grid_columnconfigure(2, weight=1, pad=0)


        # Frame izquierdo para Imagen Original
        self.left_frame = tk.Frame(self.top_frame)
        self.left_frame.grid(row=0, column=0, padx=0, pady=0)
        #Label Original Image
        self.labelO = tk.Label(
            self.left_frame,
            text= 'Imagen Original',
            font= ("Arial", 16),
            width= constants.IMG_WIDTH//10,
            anchor= 'center',
            pady=10
        
        )
        self.labelO.pack()
        
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

        # Frame derecho para Imagen no Interpolada
        self.center_frame = tk.Frame(self.top_frame)
        self.center_frame.grid(row=0, column=1, padx=0, pady=0)

        #Label Selected Quadrant
        self.labelNI = tk.Label(
            self.center_frame,
            text= 'Cuadrante no interpolado',
            font= ("Arial", 16),
            width= 385//10,
            anchor= 'center',
            pady=10
        )
        self.labelNI.pack()
        # Canvas Resultant Quadrant
        self.canvas_not_interpolated = tk.Canvas(self.center_frame, width=385, height=constants.IMG_HEIGHT)
        self.canvas_not_interpolated.pack()

        # Frame derecho para Imagen no Interpolada
        self.right_frame = tk.Frame(self.top_frame)
        self.right_frame.grid(row=0, column=2, padx=0, pady=0)

        #Label Resultant Quadrant
        self.labelI = tk.Label(
            self.right_frame,
            text= 'Cuadrante interpolado',
            font= ("Arial", 16),
            width= 385//10,
            anchor= 'center',
            pady=10
        )

        self.labelI.pack()

        self.canvas_interpolated = tk.Canvas(self.right_frame, width=385, height=constants.IMG_HEIGHT)
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
                     # Cargar imagen no interpolada
                    no_interp_img = Image.open("no_interpolada.jpg")
                    # --> Redimensionar imagen pequeña al tamaño grande
                    no_interp_img = no_interp_img.resize((385, 385), Image.NEAREST) 
                    self.tk_no_interp_img = ImageTk.PhotoImage(no_interp_img)
                    self.canvas_not_interpolated.create_image(0, 0, anchor='nw', image=self.tk_no_interp_img)
                    # Cargar imagen interpolada
                    interp_img = Image.open("interpolada.jpg")
                    self.tk_interp_img = ImageTk.PhotoImage(interp_img)
                    self.canvas_interpolated.create_image(0, 0, anchor='nw', image=self.tk_interp_img)
                else:
                    print("Número de cuadrante inválido. Debe ser entre 1 y 16.")
            except ValueError:
                print("Por favor ingrese un número válido.")
                            