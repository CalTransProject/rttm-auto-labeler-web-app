import tkinter as tk


class ReferenceObjectButton:

    def __init__(self, parent, command):
        self.button = tk.Button(
            parent,
            text="Reference Object",
            command=command,
            bg="#FFD700",
            fg="black",
            activebackground="#E6C200",
            relief="raised"
        )

    def pack(self, **kwargs):
        self.button.pack(**kwargs)

    def grid(self, **kwargs):
        self.button.grid(**kwargs)

    def place(self, **kwargs):
        self.button.place(**kwargs)

    def set_enabled(self, enabled=True):
        self.button.config(
            state="normal" if enabled else "disabled"
        )
