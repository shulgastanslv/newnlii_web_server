import json
from fastapi import APIRouter
from pydantic import BaseModel
from app.core.deepseek import OpenAIClient
from app.schemas.project import ProjectOut

router = APIRouter()

class ProjectInput(BaseModel):
    user_description: str

@router.post("/generate-project", response_model=ProjectOut)
async def generate_project(user_input: ProjectInput):
    print("Generaing ...")
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

    response = OpenAIClient.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "Ты помогаешь генерировать данные проекта."},
            {"role": "user", "content": prompt}
        ],
        stream=False
    )

    text_response = response.choices[0].message["content"]

    try:
        project_data = json.loads(text_response)
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