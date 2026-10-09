from typing import Dict, Any, List, Optional

class BoxObject:
    """Representation of a 2D Box in JPS Script."""

    def __init__(self, box_id: int, size=(100, 100), x=100, y=100):
        self.id = box_id
        self.width = size[0]
        self.height = size[1]
        self.x = x
        self.y = y
        self.dx = 3.0
        self.dy = 2.0
        self.is_running = False
        self.is_switch = False
        self.color = (0, 200, 255)  # Electric cyan

    def __repr__(self):
        return f"<BoxObject id={self.id} size=({self.width},{self.height}) running={self.is_running} switch={self.is_switch}>"

    def __str__(self):
        return self.__repr__()


class Environment:
    """Runtime environment storing variables, imported modules, and 2D game state."""

    def __init__(self):
        self.variables: Dict[str, Any] = {}
        self.box_module_imported: bool = False
        self.game_module_imported: bool = False

        self.game_size: tuple = (800, 600)
        self.game_running: bool = False

        self.boxes: List[BoxObject] = []
        self._box_counter: int = 0
        self.last_active_box: Optional[BoxObject] = None

    def set_var(self, name: str, value: Any):
        self.variables[name] = value

    def get_var(self, name: str) -> Any:
        return self.variables.get(name)

    def has_var(self, name: str) -> bool:
        return name in self.variables

    def create_box(self) -> BoxObject:
        self._box_counter += 1
        box = BoxObject(box_id=self._box_counter, size=(100, 100), x=100 + (self._box_counter * 20), y=100 + (self._box_counter * 20))
        self.boxes.append(box)
        self.last_active_box = box
        return box

    def set_last_box_size(self, width: int, height: int):
        if self.last_active_box:
            self.last_active_box.width = width
            self.last_active_box.height = height
        else:
            # Create box if none exists yet
            box = self.create_box()
            box.width = width
            box.height = height

    def enable_box_run(self):
        if self.last_active_box:
            self.last_active_box.is_running = True
        else:
            for box in self.boxes:
                box.is_running = True

    def enable_box_switch(self):
        if self.last_active_box:
            self.last_active_box.is_switch = True
        else:
            for box in self.boxes:
                box.is_switch = True
