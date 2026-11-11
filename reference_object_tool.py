
from dataclasses import asdict, dataclass
from typing import Dict, Iterable, Optional, Tuple

REFERENCE_OBJECT_CLASS = "Reference Object"
REFERENCE_OBJECT_COLOR = "#FFD700"


@dataclass
class BoundingBox:
    x: float
    y: float
    width: float
    height: float

    def __post_init__(self) -> None:
        if self.width <= 0 or self.height <= 0:
            raise ValueError("Bounding-box dimensions must be positive.")

    def move(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def resize(self, width: float, height: float) -> None:
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


class ReferenceObjectTool:
    """Draw and manage a reference-object bounding box."""

    def __init__(self) -> None:
        self.reference_object: Optional[ReferenceObject] = None
        self._drag_start: Optional[Tuple[float, float]] = None

    def start_drag(self, frame_id: str, x: float, y: float) -> None:
        """Begin drawing a new box."""
        self._drag_start = (x, y)
        self.reference_object = ReferenceObject(
            frame_id=frame_id,
            bbox=BoundingBox(x, y, 1, 1),
        )

    def update_drag(self, x: float, y: float) -> None:
        """Update the box while dragging."""
        if self._drag_start is None or self.reference_object is None:
            return

        start_x, start_y = self._drag_start

        left = min(start_x, x)
        top = min(start_y, y)
        width = max(abs(x - start_x), 1)
        height = max(abs(y - start_y), 1)

        self.reference_object.bbox = BoundingBox(
            left, top, width, height
        )

    def finish_drag(self, x: float, y: float) -> None:
        """Finish drawing the box."""
        if self._drag_start is None:
            return

        self.update_drag(x, y)
        self._drag_start = None

    def resize(self, width: float, height: float) -> None:
        """Resize the current box."""
        if self.reference_object is None:
            raise ValueError("Create a reference box first.")

        self.reference_object.bbox.resize(width, height)

    def remove(self, x: float, y: float) -> bool:
        """Remove the box if the click falls inside it."""
        obj = self.reference_object
        if obj is None:
            return False

        box = obj.bbox

        if (
            box.x <= x <= box.x + box.width
            and box.y <= y <= box.y + box.height
        ):
            self.reference_object = None
            self._drag_start = None
            return True

        return False

    def apply_to_frames(self, applier, frame_ids: Iterable[str]):
        """Apply the current box to all supplied frames."""
        if self.reference_object is None:
            raise ValueError("Create a reference box first.")

        return applier.apply_to_frames(
            self.reference_object,
            frame_ids,
        )

    def to_dict(self) -> Optional[Dict]:
        """Return the current box data."""
        if self.reference_object is None:
            return None

        return self.reference_object.to_dict()
