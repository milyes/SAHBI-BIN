# AI23N · NETSECURE PRO — Protocole IA22_LOGIC (HEXA SCELLÉE V1.6)

> **« Posséder le code ne suffit pas. »**  
> Architecture locale autonome *Zero-Trust*, sans dépendance externe, conçue pour l'audit réseau et l'exécution souveraine en mémoire vive (RAM-Only).

---

## 1. Architecture Philosophique (`IA22_LOGIC`)

Le moteur **AI23N** traduit six principes fondamentaux en règles d'exécution déterministes :

| Module | Pilier | Rôle Opérationnel |
| :--- | :--- | :--- |
| **`0001`** | **VOIX** | Émission pure, directe et sans remplissage. |
| **`0002`** | **VÉRITÉ** | Rigueur factuelle stricte, zéro extrapolation, signature HMAC-SHA256. |
| **`0003`** | **SOUVERAINETÉ** | Exécution 100 % locale (`127.0.0.1`), zéro dépendance tierce, mode *RAM-Only*. |
| **`0004`** | **ÉTHIQUE** | Limitation de débit (*Rate-Limit* 3 scans/min) et détection d'intrusion passive. |
| **`0005`** | **RÉSILIENCE** | Tampon circulaire en mémoire (`deque(maxlen=5)`) et repli souverain automatique. |
| **`0006`** | **ÉMERGENCE** | Convergence entre la sonde réseau sans privilèges root et l'analyse logique. |

---

## 2. Spécifications Techniques (`V1.6`)

* **Binaire autonome :** `ai23n_core.py` (Python 3 standard library uniquement — aucune dépendance `pip` ou `npm`).
* **Artefact d'interface :** `ai23n_cockpit.html` (interface responsive mobile/desktop).
* **Isolation Zero-Trust :**
  * Écoute stricte sur l'interface loopback `127.0.0.1:5001` (aucune exposition WAN/LAN).
  * Jeton de session cryptographique éphémère de 256 bits généré via `/dev/urandom` à chaque démarrage.
  * Validation des requêtes par comparaison à temps constant (`hmac.compare_digest`).
  * Protection anti-saturation limitée à 64 Ko par requête `POST`.
* **Sonde Réseau Sans Root (`NetSecure Pro`) :**
  * Balayage multi-thread TCP (`ports 22, 80, 443, 8080`) compatible Android / Termux sans privilèges `root`.
  * Mode **Scan Rapide** (`.1` à `.50` en ~2s) ou **Scan Complet** (`.1` à `.254`).
  * Détection différentielle des nouveaux hôtes par comparaison avec la baseline en RAM.

---

## 3. Déploiement Rapide (1-Line Build)

Exécuter dans un terminal POSIX / Linux / Termux :

```bash
chmod +x ai23n_build.sh && ./ai23n_build.sh
```

Ouvrir ensuite l'interface locale dans un navigateur isolé (Firefox ou Brave) :

```text
http://127.0.0.1:5001
```

---

## 4. Endpoints API Internes

Toutes les requêtes `POST` exigent l'en-tête d'authentification `X-AI23N-Token` :

* `POST /api/ai/scan` — Exécute l'audit sentinelle (`fast: true/false`) et scelle le rapport (`SIG:HMAC`).
* `POST /api/ai/history` — Restitue l'historique circulaire en RAM des 5 derniers audits.
* `POST /api/ai/recommendations` — Analyse automatiquement la dernière trame en mémoire (`0003 + 0004`).
* `POST /api/ai/summary` — Condense le signal réseau actif (`0001 + 0002`).
* `POST /api/ai/config/origin` — Bascule l'origine d'exécution (`AUTO` | `LOCAL` | `OPENAI`).

---

## 5. Avertissement (Labo & Recherche)

Ce logiciel est un outil d'audit et de recherche développé en local à Montréal. Il fonctionne exclusivement sur le réseau local de l'utilisateur et ne stocke aucune donnée sur disque par défaut.

*Statut : `SIGN_LOGIC::VIVANT` — Build `AI23N V1.6`*
