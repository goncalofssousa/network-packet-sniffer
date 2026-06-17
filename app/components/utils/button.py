import customtkinter as ctk

from components.app import TEXT_COLOR


def Button(parent, title, value, onClick=None, labelFrame=False):
    container = ctk.CTkFrame(
        parent,
        corner_radius=15,
        fg_color="#222222",
        height=30,
    )

    if title:
        frame = ctk.CTkFrame(
            container,
            fg_color="#1A1A1A",
        )
        frame.pack(side="left")

        label = ctk.CTkLabel(
            frame,
            text=title,
            font=("Inter 18pt SemiBold", 12),
            text_color=TEXT_COLOR,
        )
        label.pack(side="left", padx=10)

    value_label = ctk.CTkLabel(
        container,
        text=value,
        font=("Inter 18pt", 15),
        text_color=TEXT_COLOR,
    )
    value_label.pack(side=title and "left" or "top", padx=10)

    widgets = [container, value_label] + ([label] if title else [])

    def _onClick(event):
        container.configure(fg_color="#272727")
        if onClick:
            onClick()

    if title:
        for w in widgets:
            w.bind("<Button-1>", _onClick)

    if not title:
        for w in widgets:
            w.bind("<Enter>", lambda e: container.configure(fg_color="#272727"))
            w.bind("<Leave>", lambda e: container.configure(fg_color="#222222"))
            w.bind("<Button-1>", _onClick)

    return labelFrame and [container, value_label] or container
