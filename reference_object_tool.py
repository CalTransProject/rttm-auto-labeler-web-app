from typing import Iterable, Optional

from .reference_object import (
    BoundingBox,
    ReferenceObject
)


class ReferenceObjectTool:

    def __init__(
        self,
        frame_id: str = "0",
        dataset: str = "unknown"
    ):
        self.frame_id = str(frame_id)
        self.dataset = dataset
        self.reference_object: Optional[ReferenceObject] = None
        self._drag_start = None

    def set_frame(self, frame_id, dataset=None):
        self.frame_id = str(frame_id)

        if dataset is not None:
            self.dataset = dataset

    def start_drag(self, x: float, y: float):
        self._drag_start = (float(x), float(y))

    def update_drag(self, x: float, y: float):
        if self._drag_start is None:
            return None

        x0, y0 = self._drag_start

        left = min(x0, x)
        top = min(y0, y)

        width = abs(x - x0)
        height = abs(y - y0)

        if width <= 0 or height <= 0:
            return None

        return BoundingBox(
            left,
            top,
            width,
            height
        )

    def finish_drag(self, x: float, y: float):
        box = self.update_drag(x, y)
        self._drag_start = None

        if box is None:
            raise ValueError(
                "Drag to create a box with positive width and height."
            )

        self.reference_object = ReferenceObject(
            frame_id=self.frame_id,
            bbox=box,
            dataset=self.dataset
        )

        return self.reference_object

    def resize(self, width: float, height: float):
        if self.reference_object is None:
            raise RuntimeError(
                "Create a reference-object box before resizing."
            )

        self.reference_object.bbox.resize(
            width,
            height
        )

        return self.reference_object

    def move(self, x: float, y: float):
        if self.reference_object is None:
            raise RuntimeError(
                "Create a reference-object box before moving."
            )

        self.reference_object.bbox.move(x, y)

        return self.reference_object

    def remove(self):
        existed = self.reference_object is not None

        self.reference_object = None
        self._drag_start = None

        return existed

    def remove_at(self, x: float, y: float):
        if (
            self.reference_object is not None
            and self.reference_object.bbox.contains(x, y)
        ):
            return self.remove()

        return False

    def apply_to_frames(self, frame_ids: Iterable[str]):
        if self.reference_object is None:
            raise RuntimeError(
                "No reference-object box exists to apply."
            )

        results = []

        for frame_id in frame_ids:
            obj = ReferenceObject(
                frame_id=str(frame_id),
                bbox=BoundingBox(
                    **self.reference_object.bbox.to_dict()
                ),
                class_name=self.reference_object.class_name,
                color=self.reference_object.color,
                dataset=self.reference_object.dataset
            )

            results.append(obj)

        return results

    def to_dict(self):
        if self.reference_object is None:
            return None

        return self.reference_object.to_dict()
