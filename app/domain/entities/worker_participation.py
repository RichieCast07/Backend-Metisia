from dataclasses import dataclass

@dataclass
class WorkerParticipation:
    id: str
    sale_id: str
    worker_id: str
    percentage: float
