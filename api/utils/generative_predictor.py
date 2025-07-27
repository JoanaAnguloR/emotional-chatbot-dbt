import json
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Cargar el modelo.
# EMOTION PREDICTOR - HuggingFace T5 fine-tuned
# Modelo utilizado: mrm8488/t5-base-finetuned-emotion
# Fuente: https://huggingface.co/mrm8488/t5-base-finetuned-emotion

# Este modelo está entrenado para reconocer emociones en texto.
# Lo usamos aquí para identificar la emoción dominante en mensajes en español,
# formateando el prompt para alinearse con categorías de DBT.

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