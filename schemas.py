from pydantic import BaseModel

class gestor(BaseModel):
    id: int
    codigo_gestor: int
    nombre: str
    documento: str
    tipo_documento: str
    peso: int
   
    class Config:
        populate_by_name = True
        from_attributes = True