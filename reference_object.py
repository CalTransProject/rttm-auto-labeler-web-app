from dataclasses import dataclass, asdict
from typing import Any, Dict

REFERENCE_OBJECT_CLASS = "Reference Object"
REFERENCE_OBJECT_COLOR = "#FFD700"


@dataclass
class BoundingBox:
    x: float
    y: float
    width: float
    height: float

    def __post_init__(self):
        self.x = float(self.x)
        self.y = float(self.y)
        self.width = float(self.width)
        self.height = float(self.height)

        if self.width <= 0 or self.height <= 0:
            raise ValueError(
                "Bounding-box width and height must be positive."
            )

    def move(self, x: float, y: float) -> None:
        self.x = float(x)
        self.y = float(y)

    def resize(self, width: float, height: float) -> None:
        if width <= 0 or height <= 0:
            raise ValueError(
                "Width and height must be positive."
            )

        self.width = float(width)
        self.height = float(height)

    def contains(self, x: float, y: float) -> bool:
        return (
            self.x <= x <= self.x + self.width
            and self.y <= y <= self.y + self.height
        )

    def to_dict(self) -> Dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            x=data["x"],
            y=data["y"],
            width=data["width"],
            height=data["height"]
        )


@dataclass
class ReferenceObject:
    frame_id: str
    bbox: BoundingBox
    class_name: str = REFERENCE_OBJECT_CLASS
    color: str = REFERENCE_OBJECT_COLOR
    dataset: str = "unknown"

    def to_dict(self) -> Dict:
        return {
            "frame_id": str(self.frame_id),
            "class_name": self.class_name,
            "color": self.color,
            "dataset": self.dataset,
            "bbox": self.bbox.to_dict()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            frame_id=str(data["frame_id"]),
            bbox=BoundingBox.from_dict(data["bbox"]),
            class_name=data.get(
                "class_name", REFERENCE_OBJECT_CLASS
            ),
            color=data.get(
                "color", REFERENCE_OBJECT_COLOR
            ),
            dataset=data.get("dataset", "unknown")
        )
