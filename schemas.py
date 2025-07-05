from pydantic import BaseModel

class gestor(BaseModel):
    id: int
    codigo_gestor: int
    nombre: str
    documento: str
    tipo_documento: str
    peso: int
   

    class Config:
        orm_mode = True
        allow_population_by_field_name = True