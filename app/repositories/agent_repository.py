from fastapi import Depends 
from sqlalchemy import select 
from sqlalchemy.orm import Session 

from app.db import get_db 
from app.models import Agent 

class AgentRepository:
    """Repository pattern: the single access point for Agent data.

    Read-only for now (used for ticket assignment); write methods
    are added with authentication.
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    def get(self, agent_id: int) -> Agent | None:
        return self.db.get(Agent, agent_id)
    
    def list_all(self) -> list[Agent]:
        return list(self.db.scalars(select(Agent).order_by(Agent.name)).all())

def get_agent_repository(db: Session = Depends(get_db)) -> AgentRepository:
    return AgentRepository(db)