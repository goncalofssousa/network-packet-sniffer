from components.sidebar import createSideBar
from components.app import createApp
from components.dashboard import createDashboard
from components.utils.fonts import loadFonts
from src.sniffer import startSniffer, stopSniffer, getInterfaces
from tkinter import ttk


def main():
    loadFonts()
    app = createApp()
    createSideBar(app)

    if not createDashboard(app):
        return app.destroy()

    getInterfaces()
    app.mainloop()


if __name__ == "__main__":
    main()
    pass
