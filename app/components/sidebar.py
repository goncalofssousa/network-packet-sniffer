import customtkinter as ctk
import components.utils.images as images
from src.sniffer import startSniffer, stopSniffer, downloadHistory
from components.dashboard import clearActivityList
from tkinter import messagebox
from tkinter.filedialog import asksaveasfilename

def createSeparator(app):
    separator = ctk.CTkFrame(master=app, fg_color="#4B4B4B", width=1, height=app.winfo_height())
    separator.grid(row=0, column=1, sticky="ns")

def createSideBar(app):
    sideBar = ctk.CTkFrame(master=app, fg_color="transparent", width=100, corner_radius=0)
    sideBar.grid(row=0, column=0, sticky="nsew")
    sideBar.grid_rowconfigure(0, weight=0)
    sideBar.grid_rowconfigure(1, weight=0)
    sideBar.grid_rowconfigure(2, weight=0)
    sideBar.grid_rowconfigure(3, weight=0)
    sideBar.grid_columnconfigure(0, weight=1)
    sideBar.grid_propagate(False)
    createSeparator(app)
    createRefreshButton(sideBar)
    createDownloadButton(sideBar)
    createStopButton(sideBar)
    createSeparatorHorizontal(sideBar)

def createRefreshButton(sideBar):
    refreshButton = ctk.CTkButton(master=sideBar, image=images.createRefreshIcon(), text="", width=30, height=30, fg_color="transparent",hover_color="#272727")
    refreshButton.grid(row=0, column=0, pady=(25, 0))

    def refresh():
        stopSniffer()
        clearActivityList()
        sideBar.after(500, startSniffer)

    refreshButton.configure(command=refresh)

def createStopButton(sideBar):
    def on_stop_click():
        stopSniffer()
        
    stop_button = ctk.CTkButton(
        master=sideBar, 
        image=images.createStopIcon(), 
        text="", 
        width=30, 
        height=30, 
        fg_color="transparent",
        hover_color="#272727", 
        command=on_stop_click
    )
    stop_button.grid(row=1, column=0, pady=10)

def download():
    ficheiro = asksaveasfilename(
        defaultextension=".json",
        initialfile="log.json"
    )

    if ficheiro:
        downloadHistory(ficheiro)
        messagebox.showinfo(
            "Exportação concluída",
            "Ficheiro criado"
        )


def createDownloadButton(sideBar):
    refreshButton = ctk.CTkButton(master=sideBar, image=images.createDownloadIcon(), text="", width=30, height=30, fg_color="transparent",hover_color="#272727", command=download)
    refreshButton.grid(row=2, column=0)

def createSeparatorHorizontal(sideBar):
    separator = ctk.CTkFrame(master=sideBar, fg_color="#4B4B4B", width=50, height=1)
    separator.grid(row=3, column=0, pady=10)