import json
import os
from fastapi import APIRouter
from pydantic import BaseModel
from app.schemas.project import ProjectOut
from mistralai import Mistral

router = APIRouter()

class Request(BaseModel):
    user_description: str

class Result(BaseModel):
    category_id : int
    image_url : str
    budget : int
    name : str
    description : str
    crypto_type : str


@router.post("/generate-project", response_model=Result)
async def generate_project(user_input: Request):
    prompt = f"""
    На основе следующего описания пользователя:
    "{user_input.user_description}"
    Сгенерируй JSON объект проекта со следующими полями:
    - category_id: число от 1 до 10
    - image_url: строка (ссылка на изображение)
    - budget: число
    - name: название проекта
    - description: описание проекта
    - crypto_type: ETH или BTC
    Только JSON, без лишнего текста.
    """
    with Mistral(
    api_key="NoEPfEdSdUQ7tPsM4CijBlKbmMTQw6Yb",
) as mistral:

        res = mistral.chat.complete(model="mistral-small-latest", messages=[
            {
                "content": prompt,
                "role": "user",
            },
        ], stream=False)

        without_syymbols = res.choices[0].message.content.strip("```")
        result = without_syymbols.strip("json")
        print(result)
        try:
            project_data = json.loads(result)
        except json.JSONDecodeError:
            project_data = {
                "category_id": 1,
                "image_url": "",
                "budget": 0,
                "name": "Ошибка генерации",
                "description": user_input.user_description,
                "crypto_type": "ETH"
            }

        return project_data