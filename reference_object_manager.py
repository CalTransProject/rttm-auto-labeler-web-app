import json
from pathlib import Path
from typing import Dict, List, Optional

from .reference_object import ReferenceObject


class ReferenceObjectManager:

    def __init__(self, file_path="reference_objects.json"):
        self.file_path = Path(file_path)
        self._objects: Dict[str, ReferenceObject] = {}

        self.load()

    @staticmethod
    def _key(dataset, frame_id):
        return f"{dataset}::{frame_id}"

    def save_reference_object(self, obj):
        key = self._key(
            obj.dataset,
            obj.frame_id
        )

        self._objects[key] = obj
        self.save()

    def get_reference_object(self, dataset, frame_id):
        key = self._key(
            dataset,
            str(frame_id)
        )

        return self._objects.get(key)

    def remove_reference_object(self, dataset, frame_id):
        key = self._key(
            dataset,
            str(frame_id)
        )

        removed = self._objects.pop(key, None) is not None

        if removed:
            self.save()

        return removed

    def remove_all(self, dataset=None):
        if dataset is None:
            self._objects.clear()
        else:
            self._objects = {
                key: obj
                for key, obj in self._objects.items()
                if obj.dataset != dataset
            }

        self.save()

    def all_objects(self, dataset=None):
        objects = list(self._objects.values())

        if dataset is None:
            return objects

        return [
            obj for obj in objects
            if obj.dataset == dataset
        ]

    def save(self):
        self.file_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        data = [
            obj.to_dict()
            for obj in self._objects.values()
        ]

        self.file_path.write_text(
            json.dumps(data, indent=2),
            encoding="utf-8"
        )

    def load(self):
        if not self.file_path.exists():
            self._objects = {}
            return []

        data = json.loads(
            self.file_path.read_text(
                encoding="utf-8"
            )
        )

        self._objects = {}

        for item in data:
            obj = ReferenceObject.from_dict(item)

            key = self._key(
                obj.dataset,
                obj.frame_id
            )

            self._objects[key] = obj

        return list(self._objects.values())
