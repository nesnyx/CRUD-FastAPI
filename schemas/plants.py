from pydantic import BaseModel

class Plant(BaseModel):
    name:str
    family_name:str
    science_name : str
    
