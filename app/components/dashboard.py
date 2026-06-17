import customtkinter as ctk
from components.app import TEXT_COLOR
import components.utils.images as images
from components.utils.button import Button
from components.utils.functions import connectFunctions
from src.sniffer import (
    getInterfaces,
    setInterface,
    getInterface,
    getHistory,
    setFilter,
    setNextPage,
    setPreviousPage,
    setPage,
)

ActivityList = None
BeforeButton = None
AfterButton = None
PageInput = None
MaxPage = 1
PacketCounterLabel = None
Accordions = []
AccordionIndex = 0


def createDashboard(app):
    createInterfaceSelector()

    if not getInterface():
        return

    global ActivityList, PacketCounterLabel, BeforeButton, AfterButton, PageInput, StatusText

    dashboard = ctk.CTkFrame(app, fg_color="transparent")
    dashboard.grid(row=0, column=2, sticky="nsew")
    createTitle(dashboard)
    createSubTitle(dashboard)
    createInterfaceButton(dashboard)
    createSearchBar(app, dashboard)

    container = ctk.CTkFrame(master=dashboard, fg_color="transparent")
    container.pack(pady=(20, 0), padx=(0, 35), anchor="e")
    container.rowconfigure(0, weight=1)
    container.rowconfigure(1, weight=1)
    container.columnconfigure(0, weight=1)
    container.columnconfigure(1, weight=1)
    container.columnconfigure(2, weight=1)
    container.columnconfigure(3, weight=1)

    PageInput = createPageInput(container)
    StatusText = createStatusText(container)
    BeforeButton = createBeforeButton(container)
    AfterButton = createAfterButton(container)

    PacketCounterLabel = createLabel(dashboard)
    ActivityList = createActivityList(dashboard)

    createActivityListItems()

    return dashboard


def createTitle(dashboard):
    title = ctk.CTkLabel(
        dashboard,
        text="Atividade de Rede",
        font=("Inter 18pt", 32, "bold"),
        text_color=TEXT_COLOR,
    )
    title.pack(pady=(70, 0), padx=(35, 0), anchor="w")


def createSubTitle(dashboard):
    subtitle = ctk.CTkLabel(
        dashboard,
        text="Permite monitorizar e analisar toda a atividade da rede em tempo real, desde o momento em que a captura é iniciada.",
        font=("Inter 18pt Medium", 16),
        text_color="#A1A1AA",
    )
    subtitle.pack(padx=(35, 0), anchor="w")


def createInterfaceSelector(button=None):
    top = ctk.CTkToplevel()
    top.geometry(
        "700x300+"
        + str(int(top.winfo_screenwidth() / 2 + 500))
        + "+"
        + str(int(top.winfo_screenheight() / 2 + 300))
    )
    top.title("Selecionar Interface")
    top.configure(fg_color="#1A1A1A")

    container = ctk.CTkScrollableFrame(
        top,
        corner_radius=0,
        fg_color="transparent",
        scrollbar_fg_color="transparent",
        scrollbar_button_color="#1A1A1A",
        scrollbar_button_hover_color="#1A1A1A",
    )
    container.pack(pady=20, fill="both", expand=True)

    container.grid_columnconfigure(0, weight=1)
    container.grid_columnconfigure(1, weight=0)

    interfaces = getInterfaces()

    def choose(interface):
        setInterface(interface)
        if button:
            button.configure(text=interface.name)
        top.destroy()

    for i, iface in enumerate(interfaces):
        Button(container, iface.name, iface.description).grid(
            row=i, column=0, sticky="ew", padx=10, pady=5
        )
        Button(container, "", "Selecionar", lambda iface=iface: choose(iface)).grid(
            row=i, column=1
        )

    top.grab_set()
    top.wait_window()


def createInterfaceButton(dashboard):
    button = ctk.CTkButton(
        dashboard,
        text=getInterface().name,
        font=("Inter 18pt SemiBold", 16),
        fg_color="#222222",
        hover_color="#272727",
        corner_radius=15,
        width=200,
        height=50,
    )
    button.place(relx=1.0, y=70, anchor="ne", x=-35)
    button.configure(command=lambda: createInterfaceSelector(button))


def createSearchBar(app, dashboard):
    frame = ctk.CTkFrame(dashboard, corner_radius=15, fg_color="#222222")
    frame.pack(pady=(20, 0), padx=(35, 35), anchor="w", fill="x")

    icon_label = ctk.CTkLabel(
        frame, image=images.createSearchIcon(), text="", text_color=TEXT_COLOR
    )
    icon_label.pack(side="left", padx=(12, 0))

    entry = ctk.CTkEntry(
        frame,
        placeholder_text="Filtrar por atividade de rede...",
        height=50,
        font=("Inter 18pt", 16),
        fg_color="#222222",
        placeholder_text_color="#E5E7EB",
        border_width=0,
        text_color=TEXT_COLOR,
    )
    entry.pack(side="left", fill="both", expand=True, padx=(0, 15))

    def on_blur(event):
        setFilter(entry.get())
        clearActivityList()
        getHistory(page=1)

    entry.bind("<Return>", on_blur)


def createStatusText(dashboard):
    label = ctk.CTkLabel(
        dashboard,
        text="Captura Parada",
        font=("Inter 18pt SemiBold", 16),
        text_color=TEXT_COLOR,
    )
    label.grid(row=1, column=0, sticky="w", padx=(0, 10))
    return label


def createPageInput(dashboard):
    PageInput = ctk.CTkEntry(
        dashboard,
        placeholder_text="1-1",
        width=50,
        height=50,
        font=("Inter 18pt SemiBold", 16),
        fg_color="#222222",
        border_width=0,
        justify="center",
    )
    PageInput.grid(row=0, column=0, sticky="ne", padx=(0, 10))

    def on_enter(event):
        try:
            page = int(PageInput.get())
            if page < 1 or page > MaxPage:
                raise ValueError("Página Inválida")
            clearActivityList()
            setPage(page)
            getHistory()
        except:
            pass

    PageInput.bind("<Return>", on_enter)

    return PageInput


def createBeforeButton(dashboard):

    def on_click(event):
        clearActivityList()
        setPreviousPage()
        getHistory()

    container = ctk.CTkButton(
        dashboard,
        corner_radius=15,
        fg_color="#222222",
        hover_color="#272727",
        text="Anterior",
        width=160,
        height=50,
    )
    container.pack_propagate(False)

    container.bind("<Button-1>", on_click)

    return container


def showBeforeButton():
    BeforeButton.grid(row=0, column=1, sticky="ne", padx=(0, 10))


def hideBeforeButton():
    BeforeButton.grid_remove()


def setStartStatus():
    StatusText.configure(text="Captura Iniciada")


def setStopStatus():
    StatusText.configure(text="Captura Parada")


def createAfterButton(dashboard):

    def on_click(event):
        clearActivityList()
        setNextPage()
        getHistory()

    container = ctk.CTkButton(
        dashboard,
        corner_radius=15,
        fg_color="#222222",
        hover_color="#272727",
        text="Proximo",
        width=160,
        height=50,
    )
    container.pack_propagate(False)

    container.bind("<Button-1>", on_click)

    return container


def showAfterButton():
    AfterButton.grid(row=0, column=2, sticky="ne", padx=(0, 10))


def hideAfterButton():
    AfterButton.grid_remove()


def createLabel(dashboard):
    label = ctk.CTkLabel(
        dashboard,
        text="0 Resultados",
        font=("Inter 18pt SemiBold", 16),
        text_color=TEXT_COLOR,
    )
    label.pack(padx=(35, 0), anchor="w")
    return label


def clearActivityList():
    global AccordionIndex
    AccordionIndex = 0
    PacketCounterLabel.configure(text="0 Resultados")
    for accordion in Accordions:
        if not accordion:
            continue
        accordion[0].pack_forget()


def createActivityListItems():
    for i in range(10):
        Accordions.append(createAccordion(ActivityList))


def createActivityList(dashboard):
    scrollable_frame = ctk.CTkScrollableFrame(
        dashboard,
        corner_radius=0,
        fg_color="transparent",
        scrollbar_fg_color="transparent",
        scrollbar_button_color="#121213",
        scrollbar_button_hover_color="#121213",
    )
    scrollable_frame.pack(padx=(35, 20), fill="both", anchor="w", expand=True)

    scrollable_frame.bind_all(
        "<Button-4>",
        lambda e: scrollable_frame._parent_canvas.yview_scroll(-1, "units"),
    )
    scrollable_frame.bind_all(
        "<Button-5>", lambda e: scrollable_frame._parent_canvas.yview_scroll(1, "units")
    )

    return scrollable_frame


def createAccordion(parent):
    container = ctk.CTkFrame(
        parent,
        corner_radius=15,
        fg_color="#1A1A1A",
    )
    container.grid_rowconfigure(0, weight=1)
    container.grid_rowconfigure(1, weight=0)
    container.grid_columnconfigure(0, weight=1)

    header = ctk.CTkFrame(container, corner_radius=15, fg_color="transparent")
    header.grid(row=0, column=0, sticky="ew", pady=10)
    header.grid_columnconfigure(0, weight=0)
    header.grid_columnconfigure(1, weight=0)
    header.grid_columnconfigure(2, weight=0)
    header.grid_columnconfigure(3, weight=0)
    header.grid_columnconfigure(4, weight=0)
    header.grid_columnconfigure(5, weight=0)
    header.grid_columnconfigure(6, weight=1)
    header.grid_columnconfigure(7, weight=0)

    icon_label = ctk.CTkLabel(
        header, image=images.createForwardIcon(90), text="", text_color=TEXT_COLOR
    )
    icon_label.grid(row=0, column=0, padx=(10, 5))

    protocol_label = ctk.CTkLabel(
        header,
        font=("Inter 18pt SemiBold", 16),
        width=100,
        height=30,
        corner_radius=260,
        fg_color="#272727",
        text_color=TEXT_COLOR,
    )
    protocol_label.grid(row=0, column=1, padx=5)

    [details, tabview] = createDetailView(container)
    detailsOpen = False

    def onClick(event):
        nonlocal detailsOpen
        if detailsOpen:
            details.grid_remove()
            icon_label.configure(image=images.createForwardIcon(90))
            detailsOpen = False
        else:
            details.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))
            icon_label.configure(image=images.createForwardIcon(0))
            detailsOpen = True

    [button1, label_button1] = Button(header, "Fonte:", "", onClick, True)
    button1.grid(row=0, column=2, padx=5)
    [button2, label_button2] = Button(header, "Destino:", "", onClick, True)
    button2.grid(row=0, column=3, padx=5)
    [button3, label_button3] = Button(header, "Tamanho:", "", onClick, True)
    button3.grid(row=0, column=4, padx=5)
    [button4, label_button4] = Button(header, "Info:", "", onClick, True)
    button4.grid(row=0, column=5, padx=5)

    timestamp_label = ctk.CTkLabel(
        header, font=("Inter 18pt SemiBold", 16), text_color=TEXT_COLOR
    )
    timestamp_label.grid(row=0, column=7, padx=(0, 15))

    [
        connectFunctions(e, None, None, onClick)
        for e in [
            container,
            header,
            icon_label,
            protocol_label,
            timestamp_label,
        ]
    ]

    return [
        container,
        protocol_label,
        label_button1,
        label_button2,
        label_button3,
        label_button4,
        timestamp_label,
        tabview,
    ]


def editDetailView(tabview, ops):
    for [layer, tab, extra] in [
        ["layer2", "Layer 2", True],
        ["layer3", "Layer 3", True],
        ["layer4", "Layer 4", False],
    ]:
        for widget in tabview.tab(tab).winfo_children():
            widget.destroy()
        if ops[layer]:
            if extra:
                tabview2 = ctk.CTkTabview(master=tabview.tab(tab))
                tabview2.pack(fill="both", expand=True)
                for key, value in ops[layer].items():
                    if not ops[layer][key]:
                        continue
                    tabview2.add(key.upper())
                    for key2, value2 in ops[layer][key].items():
                        Button(tabview2.tab(key.upper()), key2.upper(), value2).pack(
                            anchor="w", pady=5, padx=5
                        )

            else:
                for key, value in ops[layer].items():
                    Button(tabview.tab(tab), key.upper(), value).pack(
                        anchor="w", pady=5, padx=5
                    )


def createDetailView(accordion):
    detail_view = ctk.CTkFrame(accordion, fg_color="transparent")
    tabview = ctk.CTkTabview(master=detail_view)
    tabview.pack(fill="both", expand=True)

    tabview.add("Layer 2")
    tabview.add("Layer 3")
    tabview.add("Layer 4")

    return [detail_view, tabview]


def setMaxPage(page):
    PageInput.configure(placeholder_text=f"1-{page}")


def setPacketCounter(total_count):
    PacketCounterLabel.configure(text=f"{total_count} Resultados")


def editAccordion(
    parent, packet_id, protocol, source, destination, len, summary, timestamp, packet
):
    parent[1].configure(text=f"{packet_id} | {protocol}")
    parent[2].configure(text=source if source else "-")
    parent[3].configure(text=destination if destination else "-")
    parent[4].configure(text=str(len))
    parent[5].configure(text=summary)
    parent[6].configure(text=timestamp)

    editDetailView(parent[7], packet)
    parent[0].pack(pady=(10, 0), fill="x")


def receivePacket(packet):
    global AccordionIndex
    try:
        editAccordion(
            Accordions[AccordionIndex],
            packet["packet_id"],
            packet["protocol"],
            packet["src"],
            packet["dst"],
            packet["length"],
            packet["summary"],
            packet["timestamp"],
            packet,
        )
        AccordionIndex += 1
    except Exception:
        pass


def showExportMessage(filepath):
    print(f"[EXPORT] Exportado para {filepath}")
