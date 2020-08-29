import tkinter as tk
from tkinter import ttk, CENTER
from PIL import ImageTk, Image
import os

class GUI:
    def __init__(self, _controller):
        self.controller = _controller

        margin_clr = "black"
            
        self.root = tk.Tk()
        self.root.configure(bg=margin_clr, pady=10)
        self.root.title("EMCA")
        self.root.columnconfigure(2, weight=1)

        self.f1 = tk.Frame(self.root, 
                bg=margin_clr, 
                pady=20)
        self.f2 = tk.Frame(self.root, 
                bg="gray25", 
                pady=20, 
                highlightbackground=margin_clr, 
                highlightthickness=5)
        self.f3 = tk.Frame(self.root, 
                bg="gray25", 
                pady=20, 
                highlightbackground=margin_clr, 
                highlightthickness=5)
        self.f4 = tk.Frame(self.root, 
                bg="gray25", 
                pady=20, 
                highlightbackground=margin_clr, 
                highlightthickness=5)
        
        self.f1.grid(row=1, column=1)
        self.f2.grid(row=2, column=1)
        self.f3.grid(row=3, column=1)
        self.f4.grid(row=4, column=1)
        
        self.title_label = tk.Label(self.f1, 
                text="THE EMOTION CAT", 
                bg=margin_clr,
                fg='white',
                font='Helvetica 18 bold',
                )
        self.title_label.pack(side="top") 
        
        self.name_label = tk.Label(self.f2, 
                text="Owner:", 
                bg='gray25',
                fg='white',
                font=20,
                )
        self.name_label.grid(row=1, column=0)
        
        self.combo = ttk.Combobox(self.f2, values=self.controller.get_owners())
        self.combo.grid(row=1, column=1, padx=1, pady=20)
        self.combo.bind("<<ComboboxSelected>>", self.__selectCombo)
        
        self.confirm_btn = tk.Button(self.f2, 
                text="CONFIRM", 
                width=25, 
                bg = 'medium aquamarine',
                fg='white',
                command=self.__confirmButton) 
        self.confirm_btn.grid(row=2, column=0, columnspan=2, padx=150, pady=10)
        
        self.new_name_label = tk.Label(self.f3, 
                text="New owner:", 
                bg='gray25',
                fg='white',
                font=20,
                )
        self.new_name_label.grid(row=0, column=0)
        
        self.new_name = tk.Entry(self.f3)
        self.new_name.grid(row=0, column=1)
        
        self.register_btn = tk.Button(self.f3, 
                text="REGISTER", 
                width=25, 
                bg = 'medium aquamarine',
                fg='white',
                command=self.__registerButton) 
        self.register_btn.grid(row=1, column=0, columnspan=2, padx=150, pady=10)
        
        self.epochs_label = tk.Label(self.f4, 
                text="Epochs:", 
                bg='gray25',
                fg='white',
                font=20,
                )
        self.epochs_label.grid(row=0, column=0)
        
        self.epochs = tk.Entry(self.f4)
        self.epochs.grid(row=0, column=1)
        
        self.lr_label = tk.Label(self.f4, 
                text="Learning rate:", 
                bg='gray25',
                fg='white',
                font=20,
                )
        self.lr_label.grid(row=2, column=0)
        
        self.lr = tk.Entry(self.f4)
        self.lr.grid(row=2, column=1)
        
        self.decay_label = tk.Label(self.f4, 
                text="Decay:", 
                bg='gray25',
                fg='white',
                font=20,
                )
        self.decay_label.grid(row=1, column=0)
        
        self.decay = tk.Entry(self.f4)
        self.decay.grid(row=1, column=1)
        
        self.train_btn = tk.Button(self.f4, 
                text="TRAIN", 
                width=25, 
                bg = 'medium aquamarine',
                fg='white',
                command=self.__trainButton) 
        self.train_btn.grid(row=3, column=0, columnspan=2, padx=150, pady=10)

    def __selectCombo(self, event):
        pass
        
    def __confirmButton(self):
        name = self.combo.get()
        #verificare ca e ceva selectat
        self.controller.start_emotion_prediction(name)

    def __registerButton(self):
        name = self.new_name.get()
        self.controller.register_owner(name)

    def __trainButton(self):
        lr = self.lr.get()
        decay = self.decay.get()
        epochs = self.epochs.get()
        self.controller.train(epochs, lr, decay)

    def show(self):
        self.root.mainloop()

