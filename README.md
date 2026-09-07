# Clausio

**Assistant d'instruction cybersécurité des candidatures aux marchés publics.**

Clausio aide un·e RSSI (ou un·e DPO) à instruire le volet cybersécurité et conformité des
candidatures reçues dans le cadre d'un marché public : on dépose les documents du candidat, un LLM
**pré-qualifie** chaque exigence d'un référentiel, le·la RSSI **valide ou corrige**, puis Clausio
génère un **rapport PDF** et un **fichier Excel de liaison** à renvoyer au candidat pour compléments.

L'outil n'est **pas limité à un secteur** : il couvre les référentiels transverses (RGPD pour les
DPO, NIS2, CRA, AI Act), une dizaine de **référentiels sectoriels** (santé, énergie, finance,
transport aérien, automobile, télécoms, eau, agroalimentaire, chimie, administration, spatial…) et
les dispositifs médicaux (MDR/IVDR).

> **Philosophie : « Clausio propose, le RSSI affine, la décision reste humaine. »**
> Toute sortie du LLM est une *proposition* ; rien n'est décidé automatiquement.

Clausio est **né dans l'instruction des marchés de santé** — autour du **Clausier Conformité
Numérique en Santé** (Club RSSI Santé / Club DPO / AFIB) — puis généralisé à tout marché public et
à l'instruction RGPD des DPO, en s'appuyant sur les **référentiels en vigueur** (RGPD, NIS2, CRA,
AI Act, MDR, IVDR) et les normes sectorielles applicables.

---

## Fonctionnalités

- Dépôt de documents (PDF, Word, Excel, ZIP) et extraction du texte.
- Pré-qualification par LLM de chaque exigence : `couvert` / `partiel` / `absent` /
  `non_applicable` / `à vérifier`, avec justification et passages cités.
- Recherche **hybride** (sémantique par embeddings ∪ lexicale bilingue FR↔EN) pour retrouver
  les passages pertinents, même quand le candidat reformule ou répond en anglais.
- Validation RSSI par exigence (ou en masse), avec traçabilité.
- **Catalogue de référentiels** : transverses (RGPD, NIS2, CRA, AI Act), sectoriels (santé,
  énergie, finance, aviation, automobile, télécoms, eau, agroalimentaire, chimie, administration,
  spatial) et dispositifs médicaux (MDR/IVDR) — extensible par simple ajout d'un fichier YAML.
- **Analyses liées** : instruire une même candidature sous plusieurs référentiels (onglets),
  avec indicateur de conformité agrégé.
- **Multi-utilisateurs cloisonné** : chaque dossier n'est visible que par son propriétaire (RSSI)
  et le correspondant d'établissement désigné ; l'admin gère les comptes.
- Génération d'un **rapport PDF** et d'un **fichier Excel de liaison** (réimportable).
- **Export de diagnostic** (admin) pour auditer les décisions du LLM.
- **Double authentification (MFA/TOTP)** par compte (Google Authenticator, FreeOTP, Aegis…).
- **Mise à jour des référentiels** depuis le dépôt public, en un clic, depuis l'administration.
- **Notifications par courriel (SMTP)** : à chaque mise à jour d'un dossier, les personnes qui
  l'instruisent reçoivent la liste des changements et le lien vers le dossier.
- **Coordonnées des comptes** (téléphone fixe et mobile) pour faciliter la mise en relation lors
  de l'étude de marché.
- **Choix du moteur IA** : Albert, OpenAI, Anthropic (Claude), Google (Gemini), Mistral, DeepSeek, Groq, OpenRouter, Together, ou LLM local (Ollama, vLLM, LM Studio).

---

## Aperçu

Au premier lancement, un assistant d'installation guide la configuration (conditions
d'utilisation, compte administrateur, modèle d'IA, comptes, authentification).

![Assistant d'installation](docs/06-installation.png)

Le tableau de bord regroupe les candidatures ; une candidature peut être instruite sous
plusieurs référentiels (onglets).

![Tableau de bord](docs/02-tableau-de-bord.png)

Sur un dossier : indicateur de conformité globale agrégé et bloc d'administration.

![Dossier et conformité globale](docs/03-dossier-conformite.png)

Le cœur de l'outil : Clausio *propose* un statut par exigence, le RSSI *affine* et valide.

![Décision RSSI](docs/04-decision-rssi.png)

Après renvoi du fichier de liaison par le candidat, la colonne « Déclaré » reprend ses réponses.

![Suivi du fichier de liaison](docs/05-suivi-liaison.png)

Le moteur d'IA se choisit et se configure dans l'administration — Albert, OpenAI, Claude,
Gemini, Mistral… ou un LLM local (Ollama, vLLM) pour tout garder chez soi.

![Configuration de l'IA](docs/07-config-ia.png)

La double authentification (TOTP) se règle par compte, pour renforcer la traçabilité.

![Double authentification](docs/08-securite-mfa.png)

Connexion (comptes cloisonnés ; SSO en option selon la configuration).

![Connexion](docs/01-connexion.png)

> Captures réalisées sur un jeu d'exemple anonymisé (« marché_demo »).

---

## Prérequis

- **Python 3.10+**
- Un accès à un **LLM compatible OpenAI** (Albert, OpenAI, Mistral… ou un LLM **local** :
  Ollama, vLLM, LM Studio). Sans LLM, l'application fonctionne mais tout reste « à vérifier ».

---

## Installation rapide

```bash
git clone <votre-depot> clausio && cd clausio
cp .env.example .env        # puis éditez .env (voir « Configuration du LLM »)
bash run.sh                 # Linux/macOS  (Windows : run.bat)
```

`run.sh` crée l'environnement virtuel, installe les dépendances et démarre le serveur sur
`http://127.0.0.1:3000`.

Au **premier lancement**, un **assistant d'installation** s'affiche : acceptation des conditions
d'utilisation, création du compte administrateur, choix et configuration du **modèle d'IA** (Albert,
OpenAI, Mistral ou LLM **local**), ajout de comptes, et choix du mode d'authentification (comptes
locaux ou **LDAP/AD**). La configuration du LLM peut ainsi se faire entièrement depuis l'interface,
sans toucher au `.env`. Le modèle, l'URL, la clé et la **température** restent **reconfigurables à tout moment** dans **Administration → Configuration de l'IA** (avec test de connexion).

> **Ubuntu / venv** : si la création de l'environnement échoue, installez le paquet
> `python3.X-venv` correspondant à votre version (ex. `sudo apt install -y python3.12-venv`),
> puis relancez `bash run.sh` **sans sudo**. `run.sh` choisit automatiquement la plus récente
> version de Python ≥ 3.10 disponible.

---

## Configuration du LLM

Clausio parle le **protocole OpenAI** (`/chat/completions`, `/embeddings`). Il fonctionne donc
avec n'importe quel fournisseur compatible. La configuration se fait via le fichier `.env`
(copié depuis `.env.example`) ou des variables d'environnement.

| Variable                   | Rôle                                              |
|----------------------------|---------------------------------------------------|
| `CLAUSIO_LLM_BASE_URL`     | URL de base incluant `/v1`                        |
| `CLAUSIO_LLM_API_KEY`      | Clé d'API (vide pour un LLM local)                |
| `CLAUSIO_LLM_MODEL`        | Modèle de génération (vide = auto-détection)      |
| `CLAUSIO_LLM_EMBED_MODEL`  | Modèle d'embeddings (vide = auto-détection)       |

**Exemples** (voir `.env.example` pour le détail) :

- **Albert (DINUM)** : `CLAUSIO_LLM_BASE_URL=https://albert.api.etalab.gouv.fr/v1` + votre clé.
- **OpenAI** : `https://api.openai.com/v1`, modèle `gpt-4o-mini`, embeddings `text-embedding-3-small`.
- **Mistral** : `https://api.mistral.ai/v1`, modèle `mistral-small-latest`, embeddings `mistral-embed`.
- **Ollama (local, sans clé)** :
  `CLAUSIO_LLM_BASE_URL=http://localhost:11434/v1`, `CLAUSIO_LLM_MODEL=llama3.1`,
  `CLAUSIO_LLM_EMBED_MODEL=nomic-embed-text` (après `ollama pull llama3.1` et
  `ollama pull nomic-embed-text`).
- **vLLM / LM Studio / llama.cpp** : pointez `CLAUSIO_LLM_BASE_URL` vers le serveur local.

> La **qualité de la recherche sémantique** dépend de la disponibilité d'un modèle d'embeddings
> (idéalement multilingue). Sans embeddings, Clausio se replie sur une recherche lexicale
> bilingue FR↔EN, moins fine mais fonctionnelle.

---

## Comptes et cloisonnement

- **Administration → Comptes** (admin) : créer des comptes, réinitialiser les mots de passe,
  activer/désactiver. Chaque utilisateur change son propre mot de passe.
- Un dossier n'est visible que par son **propriétaire** (le compte qui l'a créé) et le
  **correspondant d'établissement** désigné (liaison éditeur ↔ RSSI). L'admin voit tout.
- Un compte admin actif est **garanti** au démarrage (le compte `CLAUSIO_USER` est recréé/promu
  si aucun admin n'existe) : pas de verrouillage possible.

---

## Catalogue de référentiels

Le menu « Nouvelle analyse » propose plusieurs référentiels, regroupés par famille. Ajouter un
référentiel = déposer un fichier YAML dans `referentiels/` (il apparaît au redémarrage).

**Transverses (tous secteurs)**

| Référentiel | Objet | Sources principales |
|-------------|-------|---------------------|
| **RGPD** | Protection des données ; instruction d'un sous-traitant (utile aux DPO). Profils *socle* / *données de santé*. | RGPD (UE 2016/679), HDS |
| **NIS2** | Mesures de gestion des risques et notification. | Directive (UE) 2022/2555 |
| **CRA** | Exigences essentielles de cybersécurité des produits numériques. | Règlement (UE) 2024/2847 |
| **AI Act** | Conformité des systèmes d'IA. Profils *socle* / *haut risque*. | Règlement (UE) 2024/1689 |

**Secteurs économiques** (alignés NIS2 et normes du domaine)

| Référentiel | Sources principales |
|-------------|---------------------|
| **Santé** — Clausier Conformité Numérique en Santé | Club RSSI Santé / Club DPO / AFIB |
| **Énergie** | NIS2, IEC 62443, IEC 62351 |
| **Banque & Finance** | DORA (UE 2022/2554), PCI-DSS, EBA |
| **Aviation** | EASA Part-IS, DO-326A/ED-202A, DO-356A |
| **Automobile** | UNECE R155/R156, ISO/SAE 21434, TISAX |
| **Télécoms & infra numérique** | NIS2, EECC art. 40-41, 5G Toolbox |
| **Eau (potable & assainissement)** | NIS2, IEC 62443 |
| **Agroalimentaire** | NIS2, IEC 62443, ISO 27001 |
| **Chimie & pharmacie** | NIS2, IEC 62443/61511, Seveso III |
| **Administration publique** | NIS2, RGS, SecNumCloud, RGPD |
| **Spatial & aérospatial** | NIS2, ECSS, CCSDS SDLS |

**Dispositifs médicaux**

| Référentiel | Sources principales |
|-------------|---------------------|
| **MDR** | Règlement (UE) 2017/745, MDCG 2019-16 |
| **IVDR** | Règlement (UE) 2017/746, MDCG 2019-16 |

> ⚠️ **Important.** Hormis le Clausier Conformité Numérique en Santé (le plus complet et éprouvé),
> les référentiels ci-dessus sont des **extraits opérationnels** destinés à outiller l'instruction.
> Ils ne sont **pas exhaustifs** et ne se substituent pas à l'analyse de conformité réglementaire
> ni aux normes sectorielles applicables : à valider et compléter avec les experts du domaine, le
> juridique et le DPO. Les contributions pour les enrichir sont particulièrement bienvenues.

---

## Analyses liées & export de diagnostic

- **Analyse complémentaire** (bouton au tableau de bord) : instruire la même candidature sous un
  autre référentiel (RGPD pour la DPO, MDR pour le biomed…). Les analyses deviennent des onglets
  d'un même dossier ; on peut aussi **rattacher** une analyse déjà réalisée séparément.
- **Export de diagnostic** (admin, sur la page d'un dossier) : pour chaque exigence, le statut
  proposé, la confiance, la justification du LLM et les passages qui lui ont été soumis. Utile
  pour comprendre les « à vérifier ».

---

## Déploiement (VPS, accès distant)

`run.sh` écoute par défaut sur `0.0.0.0:3000`. Pour une mise en ligne propre : service **systemd**
+ reverse-proxy **Caddy** (HTTPS automatique). Fichiers et procédure dans **`deploy/`**
(`clausio.service`, `Caddyfile`, `README-deploiement.md`).

Pare-feu (Ubuntu) : n'ouvrez que ce qui est nécessaire.
```bash
sudo ufw allow OpenSSH
sudo ufw allow 80,443/tcp     # si Caddy en frontal
sudo ufw enable
```

---

## Sécurité & limites — à lire

- **Non-décision** : Clausio *propose*. La qualification finale et l'avis relèvent du·de la RSSI.
- **Données sensibles** : un VPS ou un poste ordinaire n'est **pas un hébergement conforme**
  (HDS / SecNumCloud). N'y déposez pas de vraies candidatures ni de données de santé — réservez
  ces instances à la démonstration, l'ergonomie et des dossiers non sensibles.
- **Avant toute mise en ligne** : changez `CLAUSIO_USER` / `CLAUSIO_PASSWORD`, définissez un
  `CLAUSIO_SESSION_SECRET` unique, et placez l'application derrière HTTPS.
- **Authentification** : comptes locaux, option LDAP/AD, et **double authentification (TOTP)**
  activable par compte — recommandée pour les comptes à privilèges.
- **Stockage des fichiers** : répertoires et noms de fichiers **non devinables** (jetons
  aléatoires), aucun nom fourni par le client n'est utilisé comme chemin (protection contre le
  path traversal et les accès directs devinables / IDOR).
- **Sessions** : secret de signature généré aléatoirement et persistant si non fourni ; cookie
  `SameSite=Lax` (option `CLAUSIO_HTTPS_ONLY=1` derrière HTTPS). Un plafond de taille d'upload
  est appliqué (`CLAUSIO_MAX_UPLOAD_MO`, 50 Mo par défaut).

---

## Structure du projet

```
app/            # application FastAPI (config, modèles, LLM, analyse, rapports, routes)
referentiels/   # référentiels YAML (clausier santé, NIS2, CRA, MDR, IVDR, RGPD)
templates/      # gabarits Jinja2 (interface DSFR)
deploy/         # service systemd, Caddyfile, guide de déploiement
.env.example    # modèle de configuration
run.sh / run.bat
```

---

## Contribution

Les contributions sont bienvenues (issues, correctifs, nouveaux référentiels). Merci de garder la
**documentation en français** et de respecter la philosophie de non-décision automatique.

## Remerciements

Clausio s'appuie sur le travail de la **communauté des RSSI de santé**, et en particulier sur le
**Clausier Conformité Numérique en Santé** (Club RSSI Santé / Club DPO / AFIB), ainsi que sur les
référentiels réglementaires en vigueur (RGPD, NIS2, CRA, MDR, IVDR).

Merci à la communauté des RSSI de santé pour son **combat permanent à rendre nos hôpitaux plus
sûrs**. Cet outil leur est dédié, dans l'espoir de leur faire gagner un peu de temps sur
l'instruction, pour qu'ils puissent en consacrer davantage à l'essentiel : la protection des
patients et de leurs données.

## Journal des versions

Voir [CHANGELOG.md](CHANGELOG.md) pour le détail des évolutions et des correctifs de sécurité.

## Licence

Distribué sous licence **MIT** .

---

*Clausio est un outil d'aide à l'instruction. Il ne remplace ni l'analyse humaine, ni un avis
juridique, ni une analyse de conformité réglementaire.*
