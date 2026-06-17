def connectFunctions(element, on_enter, on_leave, on_click):
    element.bind("<Enter>", on_enter)
    element.bind("<Leave>", on_leave)
    element.bind("<Button-1>", on_click)