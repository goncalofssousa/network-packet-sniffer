import customtkinter as ctk

TEXT_COLOR = "white"


def createGrid(app):
    app.grid_columnconfigure(0, weight=0)
    app.grid_columnconfigure(1, weight=0)
    app.grid_columnconfigure(2, weight=1)
    app.grid_rowconfigure(0, weight=1)


def createApp():
    app = ctk.CTk()
    largura = app.winfo_screenwidth()
    altura = app.winfo_screenheight()
    app.geometry(f"{largura}x{altura}")
    app.title("Network Sniffer")
    app.configure(fg_color="#121213")
    createGrid(app)
    return app
