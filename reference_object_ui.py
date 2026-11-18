import tkinter as tk
from reference_object_tool import ReferenceObjectTool


class ReferenceObjectUI:

    def __init__(self, canvas, frame_id=0, dataset=""):
        self.canvas = canvas
        self.tool = ReferenceObjectTool(
            frame_id,
            dataset
        )

        self.rectangle_id = None

        self.canvas.bind(
            "<ButtonPress-1>",
            self.on_mouse_down
        )

        self.canvas.bind(
            "<B1-Motion>",
            self.on_mouse_drag
        )

        self.canvas.bind(
            "<ButtonRelease-1>",
            self.on_mouse_up
        )

    def on_mouse_down(self, event):
        if self.tool.remove_at(event.x, event.y):
            if self.rectangle_id:
                self.canvas.delete(self.rectangle_id)
                self.rectangle_id = None
            return

        self.tool.start_drag(event.x, event.y)

    def on_mouse_drag(self, event):
        bbox = self.tool.update_drag(
            event.x,
            event.y
        )

        if bbox is None:
            return

        if self.rectangle_id:
            self.canvas.delete(self.rectangle_id)

        self.rectangle_id = self.canvas.create_rectangle(
            bbox.x,
            bbox.y,
            bbox.x + bbox.width,
            bbox.y + bbox.height,
            outline="#FFD700",
            width=3
        )

    def on_mouse_up(self, event):
        self.tool.finish_drag(
            event.x,
            event.y
        )
