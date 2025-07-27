"""import json
import logging
import re
import unicodedata

from fastapi import FastAPI
from pydantic import BaseModel
from rapidfuzz import fuzz
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Configuración básica
app = FastAPI()
logging.basicConfig(level=logging.INFO)

# Carga del modelo 
tokenizer = AutoTokenizer.from_pretrained(
    "mrm8488/t5-base-finetuned-emotion",
    legacy=False  # para usar el comportamiento nuevo y silenciar el warning
)
model = AutoModelForSeq2SeqLM.from_pretrained("mrm8488/t5-base-finetuned-emotion")"""

"""# Diccionario emocional modular (con variantes ampliadas)
diccionario_emocional = {
    "enojo": {
        "somaticos": [
            "puños apretados",
            "calor en rostro",
            "fruncí el ceño",
            "tensión en mandíbula",
            "mandíbula apretada",
            "siento apretada la mandíbula",
            "me aprieta la mandíbula",
            "me arde el cuello",
            "dolor en cuello"
        ],
        "cognitivos": [
            "me faltaron al respeto",
            "es injusto",
            "me ignoraron",
            "me interrumpió",
            "no debería soportarlo"
        ],
        "conductuales": ["grité", "di un portazo", "respondí mal"],
        "metaforas": ["me hierve la sangre", "explosión interna"]
    },
    "tristeza": {
        "somaticos": [
            "opresión en pecho",
            "sensación de vacío",
            "pesadez corporal",
            "lágrimas"
        ],
        "cognitivos": [
            "nada tiene sentido",
            "me siento roto",
            "no valgo",
            "soledad",
            "fracaso",
            "nostalgia"
        ],
        "conductuales": [
            "lloré",
            "me aislé",
            "dejé de hacer cosas",
            "no paro de llorar",
            "tengo ganas de llorar",
            "ganas de llorar"
        ],
        "metaforas": ["todo gris", "nube emocional"]
    },
    "miedo": {
        "somaticos": [
            "palpitaciones",
            "sudoración",
            "temblor",
            "tensión muscular",
            "boca seca",
            "mareo",
            "late a mil",
            "sudo frío",
            "no puedo dejar de temblar"
        ],
        "cognitivos": [
            "no estoy a salvo",
            "algo malo va a pasar",
            "no podré soportarlo",
            "amenaza",
            "desconocido",
            "inseguridad"
        ],
        "conductuales": ["evité", "me escondí", "me paralicé"],
        "metaforas": ["me congelé", "como en una jaula"]
    },
    "culpa": {
        "somaticos": ["peso en el pecho", "nudo en la garganta", "malestar interno"],
        "cognitivos": [
            "fallé",
            "no lo merezco",
            "soy responsable",
            "me arrepiento",
            "no puedo perdonarme"
        ],
        "conductuales": ["pedí disculpas", "evité el tema"],
        "metaforas": ["lastre emocional", "me arrastro por dentro"]
    },
    "vergüenza": {
        "somaticos": ["sonrojo", "mirar al suelo", "nerviosismo corporal"],
        "cognitivos": [
            "me juzgan",
            "me siento inferior",
            "me compararon negativamente",
            "me señalaron"
        ],
        "conductuales": ["me escondí", "evité contacto visual"],
        "metaforas": ["me sentí expuesta", "deseé desaparecer"]
    },
    "asco": {
        "somaticos": ["náusea", "piel de gallina", "rechazo físico"],
        "cognitivos": ["me repugna", "me da arcadas", "me da repelús"],
        "conductuales": ["cerré los ojos", "me alejé"],
        "metaforas": ["me revuelve el estómago", "veneno emocional"]
    },
    "alegria": {
        "somaticos": [
            "ligereza",
            "calor en el pecho",
            "energía corporal",
            "sonrisa espontánea",
            "ligero",
            "energía en todo el cuerpo",
            "sonrisa sin parar"
        ],
        "cognitivos": [
            "me siento afortunado",
            "todo está bien",
            "logré mi objetivo",
            "me siento pleno"
        ],
        "conductuales": ["celebré", "compartí", "sonreí"],
        "metaforas": ["brillo interior", "flor abierta"]
    },
    "amor": {
        "somaticos": ["calidez interna", "suspiro suave", "relajación corporal"],
        "cognitivos": ["me siento conectado", "me importa profundamente", "pienso en esa persona"],
        "conductuales": ["abrazar", "escuchar", "dar cariño"],
        "metaforas": ["como estar en casa", "abrazo emocional"]
    },
    "envidia": {
        "somaticos": ["tensión interna", "sensación de vacío"],
        "cognitivos": ["me comparo", "me molesta su éxito", "quiero lo que tiene"],
        "conductuales": ["me alejé", "evité felicitar"],
        "metaforas": ["picazón interna", "aguijón emocional"]
    },
    "celos": {
        "somaticos": ["latidos rápidos", "nudo en el estómago", "ansiedad"],
        "cognitivos": ["miedo a la pérdida", "me reemplazarán", "no soy suficiente"],
        "conductuales": ["insistí en saber", "busqué pruebas"],
        "metaforas": ["fuego interno", "tormenta en el pecho"]
    }
}

# Ponderaciones por tipo de frase
ponderaciones_tipo = {
    "somaticos": 1.5,
    "cognitivos": 1.2,
    "conductuales": 1.0,
    "metaforas": 1.3
}"""

"""def normalizar_texto(texto: str) -> str:
    texto = texto.lower()
    texto = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in texto if not unicodedata.combining(c))""" # Agregado a normalizacion.py

"""def coincide(frase_norm: str, texto_norm: str) -> bool:
    # 1. Búsqueda exacta
    if frase_norm in texto_norm:
        return True

    # 2. Coincidencia por regex de palabras completas
    tokens = [re.escape(t) for t in frase_norm.split()]
    patron = r"\b" + r"\s+".join(tokens) + r"\b"
    if re.search(patron, texto_norm):
        return True

    # 3. Fuzzy match parcial ≥ 80%
    return fuzz.partial_ratio(frase_norm, texto_norm) >= 70

def analizar_emocion(texto: str, diccionario: dict) -> dict:
    texto_norm = normalizar_texto(texto)
    scores = {}
    detalles = {}

    for emocion, categorias in diccionario.items():
        score = 0
        matches = []

        for tipo, frases in categorias.items():
            for frase in frases:
                frase_norm = normalizar_texto(frase)
                if coincide(frase_norm, texto_norm):
                    score += ponderaciones_tipo.get(tipo, 1.0)
                    matches.append((tipo, frase))

        if score > 0:
            scores[emocion] = score
            detalles[emocion] = matches

    if not scores:
        return {
            "emocion": "neutral",
            "intensidad": "sin datos",
            "detalles": [],
            "score": 0.0
        }

    emo = max(scores, key=scores.get)
    val = scores[emo]
    intensidad = (
        "alta" if val >= 3
        else "media" if val >= 1.5
        else "leve"
    )
    return {
        "emocion": emo,
        "intensidad": intensidad,
        "detalles": detalles[emo],
        "score": round(val, 2)
    }""" #Agregado a semantica_detector.py

# Clasificación generativa con T5
"""def predict_emotion_espanol(texto: str) -> dict:
    prompt = (
        f"Dado este texto: \"{texto}\"\n"
        "Clasifica la emoción principal en DBT "
        "(enojo, tristeza, culpa, vergüenza, miedo, asco, alegría, amor, envidia, celos).\n"
        "Responde en formato JSON: {\"emocion\":\"<clave>\",\"justificacion\":\"<texto>\"}"
    )
    inputs = tokenizer.encode(prompt, return_tensors="pt", max_length=512, truncation=True)
    outputs = model.generate(inputs, max_length=64)
    decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)

    try:
        return json.loads(decoded)
    except json.JSONDecodeError:
        return {"emocion": "neutral", "justificacion": ""}""" # agregado a generative_predictor.py

# Respuestas empáticas
"""respuestas_emocionales = {
    "enojo": "Siento que eso te tiene muy molesta. ¿Qué lo causó?",
    "tristeza": "Lamento que lo estés pasando. ¿Quieres compartir más?",
    "miedo": "No estás sola. ¿Hablamos de lo que te preocupa?",
    "culpa": "Entiendo esa sensación de culpa. ¿Qué crees que podrías cambiar?",
    "vergüenza": "Es duro sentirse expuesto. ¿Qué pasó que te hizo sentir así?",
    "asco": "Ese rechazo puede ser muy fuerte. ¿Quieres profundizar?",
    "alegria": "¡Me alegra oír eso! ¿Qué sucedió para que te sintieras así?",
    "amor": "Qué bonito sentir cariño. ¿Quieres contarme más?",
    "envidia": "La comparación duele. ¿Qué necesitarías para sentirte bien contigo?",
    "celos": "Los celos son normales. ¿Qué crees que los provocó?",
    "neutral": "Gracias por compartir. ¿Te gustaría seguir hablando?"
}

# Pydantic model
class MensajeInput(BaseModel):
    mensaje: str

# Endpoint con override basado en fallback semántico
@app.post("/predict/")
async def predict(data: MensajeInput):
    texto = data.mensaje
    logging.info(f"Input recibido: {texto}")

    # 1) ML generativo
    resultado_ml = predict_emotion_espanol(texto)
    emocion_ml = resultado_ml.get("emocion", "neutral")

    # 2) Fallback semántico
    resultado_fallback = analizar_emocion(texto, diccionario_emocional)

    # 3) Override si el fallback detectó algo distinto y score>0
    override = False
    emocion_final = emocion_ml
    if resultado_fallback["score"] > 0 and resultado_fallback["emocion"] != emocion_ml:
        override = True
        emocion_final = resultado_fallback["emocion"]
        logging.info(f"Override activado: {emocion_final} (score={resultado_fallback['score']})")
    else:
        logging.info(f"Emoción final (ML): {emocion_final}")

    respuesta = respuestas_emocionales.get(emocion_final, respuestas_emocionales["neutral"])
    return {
        "input": texto,
        "emocion_ml": emocion_ml,
        "emocion_final": emocion_final,
        "override": override,
        "respuesta": respuesta,
        "fallback": resultado_fallback
    }"""
