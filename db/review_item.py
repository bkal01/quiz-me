from dataclasses import dataclass, field
from datetime import date, timedelta

@dataclass
class ReviewItem:
    page_id: str
    initial_learning_date: date
    last_reviewed_date: date
    next_review_date: date
    ease_factor: float = 2.5
    review_interval: int = 1
    repetition_count: int = 0
    performance_score: float = 0.0
    priority_score: float = 0.0
    overdue_days: int = 0
    skip_counter: int = 0
    source: str = ""
    created_at: date = field(default_factory=date.today)
    last_updated_at: date = field(default_factory=date.today)
    
    
def create_new_review_item(page_id: str) -> None:
    today = date.today()
    return ReviewItem(
        page_id=page_id,
        initial_learning_date=today,
        last_reviewed_date=today,
        next_review_date=today + timedelta(1),
    )

def create_new_review_item_from_source(page_id: str, source: str) -> None:
    today = date.today()
    return ReviewItem(
        page_id=page_id,
        initial_learning_date=today,
        last_reviewed_date=today,
        next_review_date=today + timedelta(1),
        source=source,
    )