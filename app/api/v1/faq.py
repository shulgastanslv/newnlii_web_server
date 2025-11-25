from fastapi import APIRouter
from typing import List
import random
from app.schemas.faq import FAQItem

router = APIRouter()

# Всего 25 FAQ вопросов
FAQ_ITEMS = [
    {
        "question": "How long does this project typically take?",
        "answer": "The duration depends on the complexity of the project. Most projects are completed within 1-4 weeks, but this can vary based on specific requirements and revisions needed.",
    },
    {
        "question": "What is included in the budget?",
        "answer": "The budget includes the core deliverables as outlined in the project description. Any additional features or revisions beyond the initial scope may incur extra charges, which will be discussed before implementation.",
    },
    {
        "question": "Do you offer revisions?",
        "answer": "Yes, I offer revisions based on the package selected. Typically, basic packages include 1-2 revision rounds, while premium packages include unlimited revisions within the project timeline.",
    },
    {
        "question": "What payment methods do you accept?",
        "answer": "I accept various cryptocurrencies as specified in the project. Payment is typically held in escrow and released upon project completion and approval.",
    },
    {
        "question": "Can I request custom modifications?",
        "answer": "Absolutely! I'm flexible and can discuss custom requirements that align with your needs. Feel free to contact me to discuss your specific requirements.",
    },
    {
        "question": "What happens if I'm not satisfied with the final result?",
        "answer": "I'm committed to ensuring your satisfaction. If you're not happy with the result, we can discuss revisions or adjustments. The escrow system protects both parties, and we'll work together to find a solution.",
    },
    {
        "question": "How do I communicate with you during the project?",
        "answer": "Communication is done through the platform's messaging system. I typically respond within 24 hours and provide regular updates on project progress. For urgent matters, I'll make every effort to respond sooner.",
    },
    {
        "question": "Do you provide source files and documentation?",
        "answer": "Yes, all source files, documentation, and relevant materials are included in the project deliverables. You'll receive everything needed to maintain, modify, or extend the project in the future.",
    },
    {
        "question": "What if I need to cancel the project?",
        "answer": "Cancellation policies depend on the project stage. If cancellation occurs early, we can discuss a fair resolution. Once significant work has been completed, partial payment may be required based on the work done.",
    },
    {
        "question": "Can you work with my existing codebase or design?",
        "answer": "Yes, I can work with existing codebases, designs, or assets. Please share all relevant materials at the start of the project so I can understand your current setup and requirements.",
    },
    {
        "question": "Do you offer ongoing support after project completion?",
        "answer": "Basic support is typically included for a short period after delivery. Extended support, maintenance, or additional features can be arranged as a separate service if needed.",
    },
    {
        "question": "What technologies and tools do you use?",
        "answer": "I work with a wide range of modern technologies and tools depending on the project requirements. Specific technologies will be discussed during the initial consultation to ensure they align with your needs.",
    },
    {
        "question": "How do you ensure code quality and best practices?",
        "answer": "I follow industry best practices, write clean and maintainable code, include proper documentation, and test the deliverables thoroughly before delivery. Code reviews and quality checks are part of my standard process.",
    },
    {
        "question": "Can I see examples of your previous work?",
        "answer": "Yes, you can view my portfolio and previous projects on my profile. These examples showcase the quality and range of work I've completed for other clients.",
    },
    {
        "question": "What information do you need from me to start?",
        "answer": "I'll need a clear description of your requirements, any existing materials or references, your preferred timeline, and any specific constraints or preferences. The more details you provide, the better I can tailor the solution.",
    },
    {
        "question": "Do you work with teams or only individual clients?",
        "answer": "I work with both individual clients and teams. I can adapt my communication and workflow to fit your team's structure and collaboration preferences.",
    },
    {
        "question": "What if the project scope changes during development?",
        "answer": "If the scope changes significantly, we'll discuss the impact on timeline and budget before proceeding. I'm flexible and can accommodate changes, but it's important to align on any adjustments to ensure transparency.",
    },
    {
        "question": "How do you handle deadlines and project timelines?",
        "answer": "I provide realistic timelines based on project complexity and communicate any potential delays early. I'm committed to meeting agreed deadlines and will keep you informed of progress throughout the project.",
    },
    {
        "question": "Do you offer rush delivery for urgent projects?",
        "answer": "Rush delivery may be possible depending on my current workload. This typically involves a premium fee and will be discussed upfront. I'll be transparent about what's feasible within your timeframe.",
    },
    {
        "question": "What happens if you encounter technical challenges?",
        "answer": "I have experience handling various technical challenges. If unexpected issues arise, I'll communicate them promptly, propose solutions, and work with you to find the best path forward without compromising quality.",
    },
    {
        "question": "Can you integrate with third-party services or APIs?",
        "answer": "Yes, I can integrate with various third-party services, APIs, and platforms. Please specify which services you need during the initial discussion so I can confirm compatibility and plan accordingly.",
    },
    {
        "question": "Do you provide training or handover sessions?",
        "answer": "Basic handover documentation is included. If you need more detailed training or walkthrough sessions, we can arrange this as part of the project or as an additional service.",
    },
    {
        "question": "What's your policy on intellectual property and ownership?",
        "answer": "Upon full payment, you receive full ownership and rights to the deliverables. I retain the right to use the work in my portfolio unless otherwise agreed. All details are clearly outlined in the project agreement.",
    },
    {
        "question": "How do you handle multiple revisions?",
        "answer": "Revisions are handled systematically. I'll address your feedback in organized rounds, ensuring all concerns are addressed efficiently. The number of revision rounds depends on your selected package.",
    },
    {
        "question": "Can you work on projects in different time zones?",
        "answer": "Yes, I can accommodate different time zones. While there may be some delay in responses due to time differences, I'll ensure clear communication and regular updates regardless of your location.",
    },
]

@router.get("/random", response_model=List[FAQItem])
def get_random_faqs(count: int = 5):
    """
    Получить случайные FAQ вопросы.
    
    Args:
        count: Количество вопросов для возврата (по умолчанию 5, максимум 25)
    
    Returns:
        Список случайных FAQ вопросов без повторений
    """
    # Ограничиваем количество максимумом доступных вопросов
    count = min(count, len(FAQ_ITEMS))
    
    # Выбираем случайные вопросы без повторений
    selected_items = random.sample(FAQ_ITEMS, count)
    
    return [FAQItem(**item) for item in selected_items]

@router.get("/all", response_model=List[FAQItem])
def get_all_faqs():
    """
    Получить все FAQ вопросы.
    
    Returns:
        Список всех FAQ вопросов
    """
    return [FAQItem(**item) for item in FAQ_ITEMS]

