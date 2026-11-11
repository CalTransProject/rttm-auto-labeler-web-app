
from dataclasses import dataclass, asdict
from typing import Dict

REFERENCE_OBJECT_CLASS = "Reference Object"
REFERENCE_OBJECT_COLOR = "#FFD700"  # Gold


@dataclass
class BoundingBox:
    x: float
    y: float
    width: float
    height: float

    def __post_init__(self):
        if self.width <= 0 or self.height <= 0:
            raise ValueError(
                "Bounding-box width and height must be positive."
            )

    def move(self, x: float, y: float) -> None:
        """Move the box to a new top-left position."""
        self.x = x
        self.y = y

    def resize(self, width: float, height: float) -> None:
        """Change the box dimensions."""
        if width <= 0 or height <= 0:
            raise ValueError("Width and height must be positive.")

        self.width = width
        self.height = height

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class ReferenceObject:
    frame_id: str
    bbox: BoundingBox
    class_name: str = REFERENCE_OBJECT_CLASS
    color: str = REFERENCE_OBJECT_COLOR

    def to_dict(self) -> Dict:
        return {
            "frame_id": self.frame_id,
            "class_name": self.class_name,
            "color": self.color,
            "bbox": self.bbox.to_dict(),
        }
