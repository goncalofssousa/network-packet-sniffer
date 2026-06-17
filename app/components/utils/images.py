from PIL import Image
import customtkinter as ctk

def createRefreshIcon():
    return ctk.CTkImage(light_image=Image.open("images/refresh.png"), dark_image=Image.open("images/refresh.png"), size=(30, 30))

def createDownloadIcon():
    return ctk.CTkImage(light_image=Image.open("images/download.png"), dark_image=Image.open("images/download.png"), size=(30, 30))

def createStopIcon():
    return ctk.CTkImage(light_image=Image.open("images/stop.png"), dark_image=Image.open("images/stop.png"), size=(30, 30))

def createSearchIcon():
    return ctk.CTkImage(light_image=Image.open("images/search.png"), dark_image=Image.open("images/search.png"), size=(25, 25))

def createForwardIcon(rotation=0):
    return ctk.CTkImage(light_image=Image.open("images/forward.png").rotate(rotation), dark_image=Image.open("images/forward.png").rotate(rotation), size=(30, 30))