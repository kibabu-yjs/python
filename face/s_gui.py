import customtkinter as ctk, tkinter as tk, subprocess, os
from PIL import Image
scaffold = ctk.CTk()
scaffold.title("something here")
scaffold.wm_attributes("-fullscreen", True)


file_finder = f"{os.getcwd()}/face/"

def some():

    try:
        subprocess.run(['python3', f'{file_finder}try.py'])
    except Exception as err:
        print(f"sub stack:: {err}") 

btn = ctk.CTkButton(scaffold, text="just a click", command=some)
btn.grid(row=0, column=0, padx=40, pady=40)



scaffold.mainloop()