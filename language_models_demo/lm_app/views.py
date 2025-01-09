from django.shortcuts import render
from language_models_demo.secret import OPENAI_API_KEY
from transformers import pipeline
from difflib import get_close_matches
from sentence_transformers import SentenceTransformer, util
from .models import AskModel
import json
import openai

# Инициализация языковой модели
qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")
semantic_model = SentenceTransformer('all-MiniLM-L6-v2')


# Вспомогательная функция для загрузки базы знаний из модели
def get_knowledge_base():
    entries = AskModel.objects.all()
    knowledge_base = {entry.question: entry.answer for entry in entries}
    return knowledge_base


sry = "Извините, я не смог найти ответ на ваш вопрос."


# Вспомогательная функция обработки запроса
def process_query(query):
    knowledge_base = get_knowledge_base()
    knowledge_entries = list(knowledge_base.keys())
    knowledge_vectors = semantic_model.encode(knowledge_entries)

    # Попытка найти совпадение с помощью get_close_matches
    closest_match = get_close_matches(query, knowledge_entries, n=1, cutoff=0.8)
    if closest_match:
        return knowledge_base[closest_match[0]]

    # Семантический поиск
    query_vector = semantic_model.encode(query)
    scores = util.cos_sim(query_vector, knowledge_vectors)[0]
    best_match_idx = scores.argmax().item()
    if scores[best_match_idx] > 0.7:  # Проверка на порог сходства
        return knowledge_base[knowledge_entries[best_match_idx]]

    # Использование языковой модели
    context = " ".join(knowledge_base.values())
    result = qa_pipeline(question=query, context=context)
    if result and 'answer' in result and result['answer'].strip():
        # Проверяем, насколько ответ языковой модели подходит
        answer = result['answer'].strip()
        # Check confidence score and response length
        if result['score'] > 0.2 and len(answer.split()) > 2:
            return answer
        return sry


def find_value_with_model(data, question):
    # Пример запроса к языковой модели
    # замените <API_KEY> своим ключом
    openai.api_key = OPENAI_API_KEY

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Укажите модель, которую вы используете
        messages=[
            {"role": "system", "content": "Ты — помощник для работы с JSON."},
            {"role": "user", "content": f"В JSON-данных: {data}. Найди: {question}"}
        ],
        max_tokens=50
    )

    return response["choices"][0]["message"]["content"]


# View для HTML-формы
def Ask_model_view(request):
    answer = None
    if request.method == "POST":
        query = request.POST.get("query", "")
        if query:
            answer = process_query(query)
            # Пробуем обратится к OPENAI для поиска в файле
            # if answer == sry:
            #     with open("QA.json", "r" , encoding="utf-8") as json_file:
            #         data = json.load(json_file)
            #         answer = find_value_with_model(data, query)

    return render(request, 'lm_app/ask_model.html', {"answer": answer})


def Send_data(request):
    question= None
    answer=None
    user = request.user
    if user.is_superuser:
        if request.method == "POST":
            question = request.POST.get("question", "").strip()
            answer = request.POST.get("answer", "").strip()
            if question and answer:
                file_path = "QA.json"
                try:
                    # Читаем существующие данные из файла
                    try:
                        with open(file_path, "r", encoding="utf-8") as json_file:
                            data = json.load(json_file)
                    except (FileNotFoundError, json.JSONDecodeError):
                        data = []  # Если файла нет или он поврежден, создаем пустой список

                    # Проверяем наличие question и обновляем answer, если нужно
                    question_found = False
                    for entry in data:
                        if entry.get("question") == question:
                            entry["answer"] = answer  # Обновляем ответ
                            question_found = True
                            break

                    # Если вопрос отсутствует, добавляем новую запись
                    if not question_found:
                        data.append({"question": question, "answer": answer})

                    # Записываем обновленные данные в файл
                    with open(file_path, "w", encoding="utf-8") as json_file:
                        json.dump(data, json_file, indent=4, ensure_ascii=False)

                except Exception as e:
                    return render(request, 'lm_app/send_data.html', {"error": str(e)})

    return render(request, 'lm_app/send_data.html', {"question": question, "answer": answer})
