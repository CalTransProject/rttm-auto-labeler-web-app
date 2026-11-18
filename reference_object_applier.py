from reference_object import (
    ReferenceObject,
    BoundingBox
)


class ReferenceObjectApplier:

    def apply(self, reference_object, frame_ids):
        applied_objects = []

        for frame_id in frame_ids:
            bbox = BoundingBox(
                x=reference_object.bbox.x,
                y=reference_object.bbox.y,
                width=reference_object.bbox.width,
                height=reference_object.bbox.height
            )

            new_object = ReferenceObject(
                frame_id=frame_id,
                bbox=bbox,
                class_name=reference_object.class_name,
                color=reference_object.color,
                dataset=reference_object.dataset
            )

            applied_objects.append(new_object)

        return applied_objects
