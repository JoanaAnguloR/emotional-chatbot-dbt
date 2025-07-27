from pydantic import BaseModel

class MensajeInput(BaseModel):
    mensaje: str
