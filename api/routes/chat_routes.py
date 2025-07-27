from fastapi import APIRouter
import logging
from models.schemas import MensajeInput
from api.utils.generative_predictor import predict_emotion_espanol
from api.utils.semantica_detector import analizar_emocion
from api.utils.respuestas import respuestas_emocionales


router = APIRouter()
# Endpoint principal: /predict/
# Combina la salida del modelo ML con el detector semántico.
# Si el detector semántico identifica una emoción con mayor certeza, se usa como override.
# Siempre se devuelve una respuesta empática según la emoción final.

@router.post("/predict/")
async def predict(data: MensajeInput):
    texto = data.mensaje
    logging.info(f"Input recibido: {texto}")

    # Clasificación ML generativo
    resultado_ml = predict_emotion_espanol(texto)
    emocion_ml = resultado_ml.get("emocion", "neutral")

    # Fallback semántico
    resultado_fallback = analizar_emocion(texto)

    # Override (si el fallback tiene score alto y emoción distinta)
    override = False
    emocion_final = emocion_ml
    if resultado_fallback["score"] > 0 and resultado_fallback["emocion"] != emocion_ml:
        override = True
        emocion_final = resultado_fallback["emocion"]
        logging.info(f"Override activado: {emocion_final} (score={resultado_fallback['score']})")
    else:
        logging.info(f"Emoción final (ML): {emocion_final}")

    respuesta = respuestas_emocionales.get(emocion_final, respuestas_emocionales["neutral"])

# Respuesta estructurada con detalles:
# - emoción del modelo ML
# - emoción final (con o sin override)
# - respuesta empática
# - detalles del análisis semántico

    return {
        "input": texto,
        "emocion_ml": emocion_ml,
        "emocion_final": emocion_final,
        "override": override,
        "respuesta": respuesta,
        "fallback": resultado_fallback
    }
