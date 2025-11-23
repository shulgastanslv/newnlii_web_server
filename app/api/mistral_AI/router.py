import json
from typing import List, Optional, Dict, Any
from fastapi import APIRouter
from pydantic import BaseModel
from mistralai import Mistral
from app.api.mistral_AI.prompt import PROMPT_TEMPLATE, ASK_AI_PROMPT_TEMPLATE
from app.core.config import settings

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

class ProjectContext(BaseModel):
    name: str
    description: str
    budget: float
    crypto_type: int
    category: str
    skills: List[str] = []
    tags: List[str] = []

class AskAIRequest(BaseModel):
    project_id: str
    question: str
    project_context: ProjectContext

class AskAIResponse(BaseModel):
    answer: str

def generate_prompt(user_description):
    prompt = PROMPT_TEMPLATE.format(user_description=user_description)
    return prompt

def generate_ask_ai_prompt(question: str, project_context: ProjectContext):
    skills_str = ", ".join(project_context.skills) if project_context.skills else "не указаны"
    tags_str = ", ".join(project_context.tags) if project_context.tags else "не указаны"
    
    prompt = ASK_AI_PROMPT_TEMPLATE.format(
        name=project_context.name,
        description=project_context.description,
        budget=project_context.budget,
        crypto_type=project_context.crypto_type,
        category=project_context.category,
        skills=skills_str,
        tags=tags_str,
        question=question
    )
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

@router.post("/ask_ai", response_model=AskAIResponse)
async def ask_ai(request: AskAIRequest):
    prompt = generate_ask_ai_prompt(
        question=request.question,
        project_context=request.project_context
    )
    with Mistral(api_key="NoEPfEdSdUQ7tPsM4CijBlKbmMTQw6Yb") as mistral:
        res = mistral.chat.complete(model="ministral-3b-2410", messages=[
            {
                "content": prompt,
                "role": "user",
            },
        ], stream=False)
        
        answer = res.choices[0].message.content.strip()
        return AskAIResponse(answer=answer)



