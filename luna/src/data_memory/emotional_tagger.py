import re

EMOTION_PATTERNS = {
    "positive": [
        r"\b(amor|amo|adoro|feliz|alegr|content|satisf|orgulh|grat|maravilh|incr[íi]vel)\b",
        r"\b(obrigad|valeu|legal|massa|top|show|perfeito|excelente)\b",
        r"\b(||||||)\b",
    ],
    "negative": [
        r"\b(odi|raiva|trist|depress|ansios|preocup|medo|frustrad|irritad)\b",
        r"\b(merda|droga|porra|cacete|desgraça|inferno)\b",
        r"\b(|||||)\b",
    ],
    "intimate": [
        r"\b(segredo|confiss|nunca cont|só você|entre nós|particular)\b",
        r"\b(sinto falta|penso em você|especial|único|única)\b",
        r"\b(beij|abra[çc]|carin|afeto|paixão|desej)\b",
    ],
    "conflict": [
        r"\b(discord|brig|discuss|problem|errad|culp)\b",
        r"\b(não concordo|você está errad|isso é mentira)\b",
        r"\b(desculp|perdão|perdoa|arrepend)\b",
    ],
    "important": [
        r"\b(importante|essencial|fundamental|crucial|priorit)\b",
        r"\b(lembr[ae]|não esqueç|anot[ae]|guard[ae])\b",
        r"\b(meu nome|me chamo|trabalho com|moro em)\b",
    ],
}


def tag_emotion(text: str) -> dict[str, float]:
    text_lower = text.lower()
    scores = {}

    for emotion, patterns in EMOTION_PATTERNS.items():
        score = 0.0
        for pattern in patterns:
            matches = len(re.findall(pattern, text_lower, re.IGNORECASE))
            score += matches * 0.3
        scores[emotion] = min(score, 1.0)

    if all(v < 0.1 for v in scores.values()):
        scores["neutral"] = 0.5

    return scores


def get_primary_emotion(text: str) -> tuple[str, float]:
    scores = tag_emotion(text)
    if not scores:
        return ("neutral", 0.5)

    primary = max(scores.items(), key=lambda x: x[1])
    return primary


def get_emotional_context(memories: list[dict]) -> dict[str, float]:
    aggregate = {}

    for mem in memories:
        content = mem.get("content", "")
        scores = tag_emotion(content)
        for emotion, score in scores.items():
            aggregate[emotion] = aggregate.get(emotion, 0) + score

    if aggregate:
        total = sum(aggregate.values())
        if total > 0:
            aggregate = {k: v / total for k, v in aggregate.items()}

    return aggregate


def should_recall_for_emotion(memory: dict, current_emotion: str) -> float:
    content = memory.get("content", "")
    scores = tag_emotion(content)

    if current_emotion in scores:
        return scores[current_emotion]

    return 0.0


def get_emotion_intensity(text: str) -> str:
    scores = tag_emotion(text)
    max_score = max(scores.values()) if scores else 0

    if max_score >= 0.8:
        return "intenso"
    elif max_score >= 0.5:
        return "moderado"
    elif max_score >= 0.2:
        return "leve"
    else:
        return "neutro"
