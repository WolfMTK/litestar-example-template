from dataclasses import dataclass


@dataclass(slots=True)
class IdDTO:
    id: str
