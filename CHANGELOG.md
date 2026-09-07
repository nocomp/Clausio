# Journal des versions

Toutes les évolutions notables de Clausio. Format inspiré de *Keep a Changelog*.
Les versions publiques sont taguées sur le dépôt GitHub.

## [0.0.35] — 2026-08-06

### 🔧 Corrections

- **Configuration de l'IA — affichage du fournisseur.** Le réglage (URL, clé, modèle)
  était bien enregistré, mais au rechargement de la page le menu « Fournisseur »
  se réaffichait sur « Albert » au lieu du fournisseur choisi (Gemini, Claude…),
  laissant croire à une réinitialisation. Le menu reflète désormais le fournisseur
  réellement enregistré. Le texte d'aide liste les nouveaux moteurs.

## [0.0.34] — 2026-08-06

Version consolidée regroupant, pour la publication, l'ensemble des évolutions
récentes. Deux axes forts : **de nouvelles fonctionnalités** et un **durcissement
de la sécurité**.

### ✨ Nouvelles fonctionnalités

- **Ouverture à tous les secteurs.** Clausio n'est plus limité à la santé : 17
  référentiels couvrant les transverses (RGPD, NIS2, CRA, **AI Act**) et dix
  secteurs (santé, énergie, finance, aviation, automobile, télécoms, eau,
  agroalimentaire, chimie, administration, spatial), plus les dispositifs
  médicaux (MDR, IVDR). Le sous-titre devient « Assistant d'instruction
  cybersécurité des candidatures aux marchés publics ».
- **Assistant d'installation** au premier lancement : conditions d'utilisation,
  compte administrateur, choix du modèle d'IA, comptes, mode d'authentification.
- **Choix du moteur d'IA** parmi de nombreux fournisseurs compatibles OpenAI :
  Albert (DINUM), OpenAI, **Anthropic (Claude)**, **Google (Gemini)**, Mistral,
  DeepSeek, Groq, OpenRouter, Together — ou un **LLM local** (Ollama, vLLM, LM
  Studio) pour ne rien faire sortir du système d'information.
- **Double authentification (MFA/TOTP)** activable par compte, compatible Google
  Authenticator, FreeOTP, Aegis… avec activation par QR code et connexion en
  deux étapes.
- **Mise à jour des référentiels** en un clic depuis l'administration (dépôt
  GitHub configurable) : téléchargement, validation et rechargement du catalogue.
- **Notifications par courriel (SMTP)** : à chaque mise à jour d'un dossier, les
  personnes qui l'instruisent (propriétaire et correspondant) reçoivent la liste
  des changements et le lien vers le dossier.
- **Coordonnées des comptes** (téléphone fixe et mobile), utiles à la mise en
  relation lors de l'étude de marché.
- **Identité visuelle** : icône « Tuile C » (bleu France / rouge Marianne), logo
  cliquable dans l'en-tête (retour à l'accueil) et favicon.
- **Généralisation du déploiement** : configuration entièrement par variables
  d'environnement / `.env`, prise en charge de tout fournisseur compatible OpenAI,
  licence MIT, `.env.example`, `.gitignore`.

### 🔒 Sécurité

- **Uploads non prévisibles** : les répertoires et les noms de fichiers stockés
  sur le serveur sont désormais des jetons aléatoires. Le nom d'origine n'est
  conservé que comme métadonnée d'affichage — protection contre les accès directs
  devinables (IDOR).
- **Correction d'un *path traversal*** : le nom de fichier fourni par le client
  n'est plus jamais utilisé comme chemin sur le disque.
- **Correction d'une faille d'autorisation** : l'endpoint de dépôt de documents,
  jusque-là non contrôlé, exige maintenant une authentification et la visibilité
  du dossier.
- **Secret de session** généré aléatoirement et persistant si aucun n'est fourni
  (fini le secret par défaut, forgeable).
- **Cookie de session durci** : `SameSite=Lax`, option HTTPS-only derrière un
  reverse-proxy TLS, durée de vie limitée.
- **Plafond de taille** des fichiers téléversés (configurable).
- **Mots de passe** confirmés à la saisie ; l'existence d'au moins un
  administrateur actif est garantie au démarrage (anti-verrouillage).

### 🔧 Corrections

- QR code de la double authentification : rendu SVG fiable (suppression du
  prologue XML et des balises préfixées qui laissaient un carré blanc).
- Mise à jour des référentiels : message explicite en cas de limite de requêtes
  GitHub, support d'un jeton optionnel pour la lever.

---

## [0.0.26] — première diffusion publique

- Première version publiée sur GitHub, généralisée pour tout fournisseur d'IA
  compatible OpenAI, avec licence MIT, README et captures anonymisées.
- Cœur métier : import des pièces d'une candidature, pré-qualification par exigence
  proposée par l'IA, décision RSSI souveraine, génération du rapport (PDF), fichier
  de liaison (Excel) et reprise après renvoi du candidat.

> Les versions antérieures (0.0.x) correspondent au développement interne initial
> et ne sont pas distribuées.
