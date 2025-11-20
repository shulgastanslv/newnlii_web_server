import json
from fastapi import APIRouter
from pydantic import BaseModel
from mistralai import Mistral
from app.api.mistral_AI.prompt import PROMPT_TEMPLATE

router = APIRouter()

class Request(BaseModel):
    user_description: str

class Result(BaseModel):
    category_id: int
    image_url: str
    budget: float
    name: str
    description: str
    crypto_type: str

def generate_prompt(user_description):
    prompt = PROMPT_TEMPLATE.format(user_description=user_description)
    return prompt

@router.post("/generate-project", response_model=Result)
async def generate_project(user_input: Request):
    prompt = generate_prompt(user_description=user_input.user_description)
    with Mistral(api_key="NoEPfEdSdUQ7tPsM4CijBlKbmMTQw6Yb") as mistral:
        res = mistral.chat.complete(model="ministral-3b-2410", messages=[
            {
                "content": prompt,
                "role": "user",
            },
        ], stream=False)

        raw_content = res.choices[0].message.content.strip("` \n")
        if raw_content.startswith("json"):
            raw_content = raw_content[4:].strip("` \n")
        try:
            project_data = json.loads(raw_content)
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
