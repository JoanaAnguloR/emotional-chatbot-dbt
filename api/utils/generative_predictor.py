import json
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Carga del modelo una sola vez
tokenizer = AutoTokenizer.from_pretrained("mrm8488/t5-base-finetuned-emotion")
model = AutoModelForSeq2SeqLM.from_pretrained("mrm8488/t5-base-finetuned-emotion")

def predict_emotion_espanol(texto: str) -> dict:
    prompt = (
        f'Dado este texto: "{texto}"\n'
        "Clasifica la emoción principal en DBT.\n"
        "Formato: {\"emocion\":\"<clave>\",\"justificacion\":\"<texto>\"}"
    )
    inputs = tokenizer.encode(prompt, return_tensors="pt", max_length=512, truncation=True)
    outputs = model.generate(inputs, max_length=64)
    decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)

    try:
        return json.loads(decoded)
    except json.JSONDecodeError:
        return {"emocion": "neutral", "justificacion": ""}