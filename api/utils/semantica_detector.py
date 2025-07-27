from rapidfuzz import fuzz
import re
from api.utils.normalizacion import normalizar_texto

# Diccionario modular de emociones
# Construido con frases semánticas divididas por tipo
# cada emoción contiene subcategorías: somáticos, cognitivos, conductuales, metáforas

diccionario_emocional = diccionario_emocional = {
    "enojo": {
        "somaticos": [
            "puños apretados",
            "calor en rostro",
            "fruncí el ceño",
            "tensión en mandíbula",
            "mandíbula apretada",
            "siento apretada la mandíbula",
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
# Se usa para dar mayor peso a lo somático, metáforas y cognitivo vs. conducta observable

ponderaciones_tipo = {
    "somaticos": 1.5,
    "cognitivos": 1.2,
    "conductuales": 1.0,
    "metaforas": 1.3
}

# Función auxiliar para verificar si una frase coincide parcialmente con el texto

def coincide(frase_norm: str, texto_norm: str) -> bool:
    if frase_norm in texto_norm:
        return True

    tokens = [re.escape(t) for t in frase_norm.split()]
    patron = r"\b" + r"\s+".join(tokens) + r"\b"
    if re.search(patron, texto_norm):
        return True

    return fuzz.partial_ratio(frase_norm, texto_norm) >= 70

def analizar_emocion(texto: str) -> dict:
    texto_norm = normalizar_texto(texto)
    scores = {}
    detalles = {}

    for emocion, categorias in diccionario_emocional.items():
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
    intensidad = "alta" if val >= 3 else "media" if val >= 1.5 else "leve"
    return {
        "emocion": emo,
        "intensidad": intensidad,
        "detalles": detalles[emo],
        "score": round(val, 2)
    }
# Devuelve emoción detectada, intensidad basada en score,
# frases coincidentes y valor total acumulado
