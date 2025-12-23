from dataclasses import dataclass
from fastapi import status
from typing import Any, Optional, Dict

@dataclass
class APIResponse():
    status:status
    data:Optional[Any]
    message:Optional[str]
    
    
    def to_dict(self)->Dict:
        return {
            'status':self.status,
            'data':self.data,
            'message':self.message
        }