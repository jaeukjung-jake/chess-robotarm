from dataclasses import dataclass, field
from mirobot.mirobot_status import MirobotAngles

@dataclass
class SomeClass:
    angle: MirobotAngles = field(default_factory=MirobotAngles)
