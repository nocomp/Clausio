"""Client LLM générique (protocole OpenAI : /chat/completions, /embeddings).

Fonctionne avec tout fournisseur compatible OpenAI : Albert (DINUM), OpenAI, Mistral,
Azure, Groq… ou un LLM LOCAL (Ollama, vLLM, LM Studio, llama.cpp — sans clé).
On l'utilise pour QUALIFIER une exigence à partir de passages et PRÉ-REMPLIR des
métadonnées — jamais pour décider. Toute sortie est une PROPOSITION.

Le modèle de génération et le modèle d'embeddings sont auto-détectés via GET /models,
sauf si CLAUSIO_LLM_MODEL / CLAUSIO_LLM_EMBED_MODEL sont fournis. En l'absence de
service joignable, les fonctions renvoient un repli hors ligne (statut « à vérifier »).
"""
import json
from dataclasses import dataclass

import httpx

from . import settings as _settings

STATUTS_VALIDES = {"couvert", "partiel", "absent", "non_applicable", "a_verifier"}
_CACHE = {"url": None, "gen": None, "emb": None}


def _normaliser_base(url: str) -> str:
    """Accepte une URL de base (…/v1) OU un endpoint complet collé par erreur
    (…/v1/chat/completions, …/embeddings, …/models) et renvoie la base."""
    u = (url or "").strip().rstrip("/")
    for suffixe in ("/chat/completions", "/completions", "/embeddings", "/responses", "/models"):
        if u.endswith(suffixe):
            u = u[: -len(suffixe)]
    return u.rstrip("/")


def _R() -> dict:
    """Réglages LLM effectifs (base de données, repli .env), URL normalisée."""
    r = dict(_settings.llm_effectif())
    r["base_url"] = _normaliser_base(r.get("base_url", ""))
    return r


def reset_cache() -> None:
    """À appeler après modification de la configuration (assistant / administration)."""
    _CACHE.update(url=None, gen=None, emb=None)


def tester_connexion(base_url: str, api_key: str) -> dict:
    """Teste un fournisseur LLM (GET /models). Renvoie {ok, modeles, embeddings, erreur}."""
    base_url = _normaliser_base(base_url)
    if not base_url:
        return {"ok": False, "erreur": "URL manquante."}
    entetes = {"Authorization": f"Bearer {api_key}"} if api_key else {}
    try:
        r = httpx.get(f"{base_url}/models", headers=entetes, timeout=15)
        r.raise_for_status()
        data = r.json().get("data", [])
        ids = [m.get("id") or m.get("model") for m in data]
        emb = [m.get("id") or m.get("model") for m in data
               if "embed" in str(m.get("type", "")).lower() or "embed" in str(m.get("id", "")).lower()]
        return {"ok": True, "modeles": [i for i in ids if i][:50], "embeddings": emb[:20]}
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "erreur": str(e)[:200]}


def _sync(url: str) -> None:
    if _CACHE["url"] != url:
        _CACHE.update(url=url, gen=None, emb=None)


def _est_local(url: str) -> bool:
    u = (url or "").lower()
    return any(h in u for h in ("localhost", "127.0.0.1", "0.0.0.0",
                                "host.docker.internal", "::1"))


def disponible() -> bool:
    r = _R()
    # Un LLM local (Ollama, vLLM...) ne requiert pas de clé.
    return bool(r["api_key"]) or _est_local(r["base_url"])


def _entetes(api_key: str) -> dict:
    return {"Authorization": f"Bearer {api_key}"} if api_key else {}


def _modele_embeddings() -> str | None:
    """Détecte un modèle d'embeddings sur Albert (pour la recherche sémantique)."""
    reg = _R(); _sync(reg["base_url"])
    if reg["embed_model"]:
        return reg["embed_model"]
    if _CACHE["emb"]:
        return _CACHE["emb"]
    if not disponible():
        return None
    try:
        r = httpx.get(f"{reg['base_url']}/models", headers=_entetes(reg["api_key"]), timeout=20)
        r.raise_for_status()
        data = r.json().get("data", [])
        emb = [m for m in data if "embed" in str(m.get("type", "")).lower()
               or "embed" in str(m.get("id", "")).lower()]
        if emb:
            _CACHE["emb"] = emb[0].get("id") or emb[0].get("model")
            return _CACHE["emb"]
    except Exception:  # noqa: BLE001
        return None
    return None


def embeddings(textes: list[str], batch: int = 48) -> list[list[float]] | None:
    """Renvoie un vecteur par texte (recherche sémantique), ou None si indisponible."""
    reg = _R()
    modele = _modele_embeddings()
    if not (disponible() and modele and textes):
        return None
    vecteurs: list[list[float]] = []
    try:
        for i in range(0, len(textes), batch):
            lot = [t[:2000] if t else " " for t in textes[i:i + batch]]
            r = httpx.post(
                f"{reg['base_url']}/embeddings",
                headers=_entetes(reg["api_key"]),
                json={"model": modele, "input": lot},
                timeout=60,
            )
            r.raise_for_status()
            for item in r.json().get("data", []):
                vecteurs.append(item.get("embedding") or [])
        return vecteurs if len(vecteurs) == len(textes) else None
    except Exception:  # noqa: BLE001
        return None


def _modele() -> str | None:
    reg = _R(); _sync(reg["base_url"])
    if reg["model"]:
        return reg["model"]
    if _CACHE["gen"]:
        return _CACHE["gen"]
    if not disponible():
        return None
    try:
        r = httpx.get(f"{reg['base_url']}/models", headers=_entetes(reg["api_key"]), timeout=20)
        r.raise_for_status()
        data = r.json().get("data", [])
        gen = [m for m in data if str(m.get("type", "")).startswith("text-generation")]
        choix = (gen or data)
        if choix:
            _CACHE["gen"] = choix[0].get("id") or choix[0].get("model")
            return _CACHE["gen"]
    except Exception:  # noqa: BLE001
        return None
    return None


def _chat(messages: list[dict], temperature: float | None = None, timeout: int = 60) -> str | None:
    reg = _R()
    modele = _modele()
    if not (disponible() and modele):
        return None
    temp = reg.get("temperature") if temperature is None else temperature
    if temp is None:
        temp = 0.0
    try:
        r = httpx.post(
            f"{reg['base_url']}/chat/completions",
            headers=_entetes(reg["api_key"]),
            json={"model": modele, "temperature": temp, "messages": messages},
            timeout=timeout,
        )
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]
    except Exception:  # noqa: BLE001
        return None


def _nettoyer_json(texte: str) -> str:
    t = (texte or "").strip()
    if t.startswith("```"):
        t = t[3:]
        t = t[4:].strip() if t.lower().startswith("json") else t
        t = t.rsplit("```", 1)[0].strip()
    return t


def chat_json(systeme: str, utilisateur: str) -> dict:
    """Appel générique renvoyant un dict JSON (vide si indisponible/échec)."""
    brut = _chat([{"role": "system", "content": systeme},
                  {"role": "user", "content": utilisateur}])
    if not brut:
        return {}
    try:
        return json.loads(_nettoyer_json(brut))
    except Exception:  # noqa: BLE001
        return {}


@dataclass
class PropositionIA:
    statut: str
    justification: str
    confiance: float
    passages: list[dict]


_SYSTEME = (
    "Tu es un assistant d'instruction cybersécurité pour un marché public. "
    "Tu n'attribues jamais le marché et tu ne décides rien : tu qualifies UNE exigence "
    "au regard des seuls passages fournis. "
    "IMPORTANT — juge sur le FOND, pas sur la lettre : le candidat peut couvrir l'exigence "
    "avec un vocabulaire, une formulation ou une structure DIFFÉRENTS de l'énoncé. Reconnais "
    "les synonymes, paraphrases, équivalences techniques et normatives (ex. 'chiffrement au repos' "
    "≈ 'données chiffrées sur disque' ; 'MFA' ≈ 'double authentification'). "
    "Les passages peuvent être rédigés en ANGLAIS alors que l'exigence est en français "
    "(ex. 'encryption'=chiffrement, 'backup'=sauvegarde, 'authentication'=authentification, "
    "'logging'=journalisation, 'network segmentation'=cloisonnement) : évalue le fond quelle que "
    "soit la langue. "
    "Barème du statut : "
    "'couvert' si le fond de l'exigence est démontré, même formulé autrement ; "
    "'partiel' si le sujet est traité mais incomplet, imprécis, ou seulement adossé à une "
    "certification générale (CE, ISO) sans détail sur le point précis demandé ; "
    "'absent' si AUCUN passage ne traite le sujet ; "
    "'a_verifier' seulement si des passages PERTINENTS existent mais restent ambigus ou "
    "contradictoires au point d'empêcher de trancher — ce n'est ni la valeur par défaut, ni le "
    "statut à mettre quand il n'y a rien (dans ce cas c'est 'absent') ; "
    "'non_applicable' si l'exigence ne concerne pas l'objet (ex. hébergement pour une solution "
    "installée on-premise chez le client). "
    "N'invente pas : appuie chaque affirmation sur un extrait cité. "
    "Réponds STRICTEMENT en JSON : "
    '{"statut": "couvert|partiel|absent|non_applicable|a_verifier", '
    '"justification": "...", "confiance": 0.0, '
    '"passages": [{"document_nom": "...", "page": 0, "section": "...", "extrait": "..."}]}'
)


def confronter_exigence(libelle: str, question_rag: str, criteres: list[str],
                        passages_candidats: list[dict]) -> PropositionIA:
    if not disponible():
        return _stub(passages_candidats)
    contexte = "\n\n".join(
        f"[{p.get('document_nom','?')} p.{p.get('page','?')} {p.get('section','')}]\n{p.get('extrait','')}"
        for p in passages_candidats
    ) or "(aucun passage pertinent retrouvé dans la candidature)"
    user = (
        f"EXIGENCE : {libelle}\n"
        f"CE QU'IL FAUT VÉRIFIER : {question_rag}\n"
        f"CRITÈRES D'ACCEPTATION :\n- " + "\n- ".join(criteres or ["(non précisés)"]) + "\n\n"
        f"PASSAGES EXTRAITS DE LA CANDIDATURE :\n{contexte}"
    )
    data = chat_json(_SYSTEME, user)
    if not data:
        return PropositionIA("a_verifier",
                             "Qualification IA indisponible. Arbitrage humain requis.",
                             0.0, passages_candidats)
    statut = data.get("statut", "a_verifier")
    if statut not in STATUTS_VALIDES:
        statut = "a_verifier"
    return PropositionIA(statut, data.get("justification", ""),
                         float(data.get("confiance", 0.0) or 0.0),
                         data.get("passages", []) or passages_candidats)


def _stub(passages: list[dict]) -> PropositionIA:
    return PropositionIA(
        "a_verifier",
        "Mode hors ligne (clé Albert absente) : aucune qualification automatique.",
        0.0, passages)
