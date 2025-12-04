from dataclasses import dataclass
from typing import Optional

from .receiver import Receiver


@dataclass
class IBIndex:
    """
    Command pattern implementation.
    Follow the Portfolio protocol.
    """
    deposit: float
    receiver: Optional[Receiver] = None

    def survey(self) -> None:
        # TODO: Implement survey, receiver(s) etc
        if self.receiver is not None:
            return self.receiver.action()
        return None
