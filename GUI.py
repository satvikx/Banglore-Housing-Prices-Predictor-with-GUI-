import customtkinter
from PIL import Image
import os
import pandas as pd
import numpy as np
import pickle

current_path = os.path.dirname(os.path.realpath(__file__))
data = pd.read_csv(current_path+"/Cleaned_Data.csv")
locn = data['location'].unique().tolist()
pipe = pickle.load(open(current_path + "/RidgeModel.pkl",'rb'))

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")  

class App(customtkinter.CTk):
    width = 900
    height = 600

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Banglore House Prices Predictor")
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(False, False)

        # load and create background image
        
        self.bg_image = customtkinter.CTkImage(Image.open(current_path + "/bg.jpg"),
                                               size=(self.width, self.height))
        self.bg_image_label = customtkinter.CTkLabel(self, image=self.bg_image)         #LOGO
        self.bg_image_label.grid(row=0, column=0)

        # configure grid layout (4x4)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure((0,1,2,3), weight=1)


        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")

        self.sidebar_frame.grid_rowconfigure(0, weight=2)
        self.sidebar_frame.grid_rowconfigure(1, weight=1)
        self.sidebar_frame.grid_rowconfigure(2, weight=1)
        self.sidebar_frame.grid_rowconfigure(3, weight=1)
        # self.sidebar_frame.grid_rowconfigure(4, weight=1)
        # self.sidebar_frame.grid_rowconfigure(5, weight=1)

        #HOUSE IMAGE
        img = customtkinter.CTkImage(Image.open(current_path + "/h.png"),size=(160,100))

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame,image=img, text=" ")
        self.logo_label.grid(row=0, column=0, padx=5, pady=(20, 20), sticky='n')
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Clear")
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=0, sticky='n')
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Save")
        self.sidebar_button_2.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, text="Made By-",font=customtkinter.CTkFont(weight="bold"),corner_radius=20, hover_color="#54b038", command= self.made_by)
        self.sidebar_button_3.grid(row=2, column=0, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=3, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"], command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=3, column=0, padx=20, pady=(30, 30),sticky='s')
        self.appearance_mode_optionemenu.set("Dark")
        

        #HEAD
        #self.head = customtkinter.CTkFrame(self)  
        self.heading = customtkinter.CTkLabel(self, text="Predict House Prices in Banglore with Ease.",font=customtkinter.CTkFont(family = "Agency FB",size=40, weight="bold"), width=712)
        self.heading.grid(row=0, column=1, columnspan=2,pady= (20,10), sticky="n") 
        self.heading2 = customtkinter.CTkLabel(self, text="Get started by Entering Details Below!",font=customtkinter.CTkFont(family = "Century Gothic",size=20))
        self.heading2.grid(row=0, column=1, columnspan=2,padx= 57,pady= (80,10), sticky="nw")     
        self.heading.grid_columnconfigure(0, weight=2)
           

        self.frame = customtkinter.CTkFrame(self, width = 640, height=300,corner_radius=30, border_width=1, border_color="#38393b", fg_color="transparent")
        self.frame.grid(row=0, column=1, padx=(10, 0), pady=(10, 0))

        # create LOCATION combobox
        self.location = customtkinter.CTkLabel(self,text="Location:",font=customtkinter.CTkFont(family = "Calibri",size=20, weight='bold'))
        #self.location.grid(row=0, column=1,sticky= 'w')
        self.location.place(x = 250, y = 200)    
        self.combobox = customtkinter.CTkComboBox(self,border_width=1, values=locn, width=200, corner_radius=20)
        self.combobox.place(x = 250, y = 230) 
        self.combobox.set("Enter Location")       

        #SQFT Progressbar
        current_value = customtkinter.DoubleVar()
        def get_current_value():
            return '{: .2f}'.format(current_value.get())
        def slider_changed(event):
            value_label.configure(text=get_current_value())
        self.sqft = customtkinter.CTkLabel(self,text="Square ft:",font=customtkinter.CTkFont(family = "Calibri",size=20, weight='bold'))
        self.sqft.place(x = 560, y = 200)    
        self.slider = customtkinter.CTkSlider(self,variable=current_value,command=slider_changed, from_=300, to=3000, number_of_steps=2700, width=230, progress_color="white", corner_radius=20)
        self.slider.place(x = 556, y = 240)

        value_label = customtkinter.CTkLabel(
            self, font=customtkinter.CTkFont(family = "Calibri",size=30),
            text=get_current_value()
        )
        value_label.place(x=670, y=195)

        #Bath
        self.bath = customtkinter.CTkLabel(self,text="Bathrooms:",font=customtkinter.CTkFont(family = "Calibri",size=20, weight='bold'))
        self.bath.place(x = 250, y = 340)
        self.bath1 = customtkinter.CTkEntry(self, placeholder_text="Enter no. of Bathrooms", width=200, border_width=1, corner_radius=20)
        self.bath1.place(x = 250, y = 370)
        
        #Bhk
        self.bhk = customtkinter.CTkLabel(self,text="BHK:",font=customtkinter.CTkFont(family = "Calibri",size=20, weight='bold'))
        self.bhk.place(x = 560, y = 340)
        self.bhk1 = customtkinter.CTkEntry(self, placeholder_text="Enter no. of BHK", width=200, border_width=1, corner_radius=20)
        self.bhk1.place(x = 560, y = 370)

        #predict btn
        self.predict = customtkinter.CTkButton(self, text="Predict Price", width=160, font=customtkinter.CTkFont(family = "Berlin Sans FB",size=25),
                                     height=48, hover=True, hover_color="#54b038", corner_radius=30, command = self.pred)
        self.predict.place(x = 270, y = 430)

    #Prediction Engine
    def pred(self):
        locat = self.combobox.get()
        sqf = int(self.slider.get())
        bat = float(self.bath1.get())
        bh = float(self.bhk1.get())
        #print(locat, sqf, bat, bh)
        Input = pd.DataFrame([[locat, sqf, bat, bh]], columns=['location', 'total_sqft', 'bath', 'bhk'])
        prediction = pipe.predict(Input)[0] * 1e6
        p = np.round(prediction,2)

        self.pred = customtkinter.CTkLabel(self,text='Estimated Cost :                 ₹  {:,}'.format(p), text_color="#54b038",
                                font=customtkinter.CTkFont(family = "Calibri",size=30, weight='bold'))
        self.pred.place(x = 250, y = 530)
    

    #Dark Theme Switch
    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode) 

    def made_by(self):
        dialog = customtkinter.CTkInputDialog(text="Made By:  Satvik Shrivastava\nsatvik.shrivastava.exe@gmail.com\nDataset downloaded from Kaggle\nML Algorithm Used:  Ridge", title="Satvik Shrivastava")
        #print("CTkInputDialog:", dialog.get_input())




if __name__ == "__main__":
    app = App()
    app.mainloop()