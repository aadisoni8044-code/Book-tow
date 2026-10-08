"""
JPS Script Box Module Runtime
Handles body_2D.box(), size.box(), run.box(), switch.box() logic.
"""

class JPSBoxObject:
    def __init__(self, box_id):
        self.box_id = box_id
        self.width = 100
        self.height = 100
        self.is_running = False
        self.is_interactive = False # switch.box() drag & drop

    def __repr__(self):
        state = "running" if self.is_running else "static"
        inter = " interactive" if self.is_interactive else ""
        return f"<JPSBox #{self.box_id} {self.width}x{self.height} ({state}{inter})>"

class BoxRuntimeManager:
    def __init__(self):
        self.reset()

    def reset(self):
        self.box_count = 0
        self.current_box = None
        self.boxes = []

    def body_2D_box(self):
        self.box_count += 1
        box = JPSBoxObject(self.box_count)
        self.boxes.append(box)
        self.current_box = box
        return f"[JPS Box #{box.box_id} Created]"

    def size_box(self, width, height):
        if not self.current_box:
            self.body_2D_box()
        self.current_box.width = int(width)
        self.current_box.height = int(height)
        return f"[JPS Box #{self.current_box.box_id} Size set to {width}x{height}]"

    def run_box(self):
        if not self.current_box:
            self.body_2D_box()
        self.current_box.is_running = True
        return f"[JPS Box #{self.current_box.box_id} Dynamic Movement Engine Started]"

    def switch_box(self):
        if not self.current_box:
            self.body_2D_box()
        self.current_box.is_interactive = True
        return f"[JPS Box #{self.current_box.box_id} Interactive Drag-and-Drop Enabled]"
