from pydantic import BaseModel

class FAQItem(BaseModel):
    question: str
    answer: str

    class Config:
        from_attributes = True

