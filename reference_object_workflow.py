from reference_object_tool import ReferenceObjectTool
from reference_object_manager import ReferenceObjectManager
from reference_object_applier import ReferenceObjectApplier
from reference_object_exporter import ReferenceObjectExporter


class ReferenceObjectWorkflow:

    def __init__(self):
        self.tool = ReferenceObjectTool()
        self.manager = ReferenceObjectManager()
        self.applier = ReferenceObjectApplier()
        self.exporter = ReferenceObjectExporter()

    def create_reference_object(self, frame_id, dataset, x1, y1, x2, y2):
        self.tool.frame_id = frame_id
        self.tool.dataset = dataset

        self.tool.start_drag(x1, y1)
        reference_object = self.tool.finish_drag(x2, y2)

        if reference_object:
            self.manager.add(reference_object)

        return reference_object

    def remove_reference_object(self, dataset, frame_id):
        return self.manager.remove(dataset, frame_id)

    def apply_to_frames(self, reference_object, frame_ids):
        objects = self.applier.apply(
            reference_object,
            frame_ids
        )

        for obj in objects:
            self.manager.add(obj)

        return objects

    def export(self, dataset, output_path):
        objects = [
            obj
            for (obj_dataset, _), obj
            in self.manager.objects.items()
            if obj_dataset == dataset
        ]

        return self.exporter.export(
            objects,
            output_path
        )
