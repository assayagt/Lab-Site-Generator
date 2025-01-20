from enum import Enum

class ApprovalStatus(Enum):
    INITIAL_PENDING = "Initial pending approval"
    FINAL_PENDING = "Final pending approval"
    APPROVED = "Approved"
    REJECTED = "Rejected"