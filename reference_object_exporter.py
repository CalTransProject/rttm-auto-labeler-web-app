import json
from pathlib import Path


class ReferenceObjectExporter:

    def export(self, reference_objects, output_path):
        output_path = Path(output_path)

        data = [
            obj.to_dict()
            for obj in reference_objects
        ]

        output_path.write_text(
            json.dumps(data, indent=4)
        )

        return output_path
