#!/usr/bin/env python3
from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass(frozen=True)
class Task:
    id: str
    title: str
    completed: bool = False

@dataclass(frozen=True)
class Action:
    kind: str
    source_id: str
    target_id: Optional[str] = None
    completed: Optional[bool] = None
    title: Optional[str] = None

class SyncState:
    """Deterministic core for a bidirectional task sync.

    This deliberately models only state/mapping decisions. Real Craft/Todoist
    HTTP calls belong at the adapter boundary (e.g. n8n HTTP Request nodes).
    """

    def __init__(self):
        self.craft_to_todoist: Dict[str, str] = {}
        self.todoist_to_craft: Dict[str, str] = {}

    def register_pair(self, craft_id: str, todoist_id: str) -> None:
        current_t = self.craft_to_todoist.get(craft_id)
        current_c = self.todoist_to_craft.get(todoist_id)
        if current_t and current_t != todoist_id:
            raise ValueError(f"Craft task {craft_id} already maps to {current_t}")
        if current_c and current_c != craft_id:
            raise ValueError(f"Todoist task {todoist_id} already maps to {current_c}")
        self.craft_to_todoist[craft_id] = todoist_id
        self.todoist_to_craft[todoist_id] = craft_id

    def from_craft(self, craft: Task, todoist: Optional[Task] = None) -> List[Action]:
        mapped = self.craft_to_todoist.get(craft.id)
        if mapped is None:
            # Never deduplicate by title: two same-title tasks may be distinct.
            return [Action("CREATE_TODOIST", source_id=craft.id,
                           completed=craft.completed, title=craft.title)]

        if todoist is None:
            return [Action("FETCH_TODOIST_FOR_REPAIR", source_id=craft.id,
                           target_id=mapped)]

        if todoist.id != mapped:
            raise ValueError("Adapter supplied a Todoist task that does not match mapping")

        if todoist.completed != craft.completed:
            return [Action("SET_TODOIST_COMPLETED", source_id=craft.id,
                           target_id=todoist.id, completed=craft.completed)]
        return []

    def from_todoist(self, todoist: Task, craft: Optional[Task] = None) -> List[Action]:
        mapped = self.todoist_to_craft.get(todoist.id)
        if mapped is None:
            # v1 is Craft-originated creation. Unmapped Todoist tasks are ignored
            # rather than guessed/matched by title.
            return []

        if craft is None:
            return [Action("FETCH_CRAFT_FOR_REPAIR", source_id=todoist.id,
                           target_id=mapped)]

        if craft.id != mapped:
            raise ValueError("Adapter supplied a Craft task that does not match mapping")

        if craft.completed != todoist.completed:
            return [Action("SET_CRAFT_COMPLETED", source_id=todoist.id,
                           target_id=craft.id, completed=todoist.completed)]
        return []
