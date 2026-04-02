# Journal des itérations

---

## Session 001 — 2026-04-02 — Initialisation depuis description.md

**Input :** `description.md` — document de consultation, refonte SI métier Entreprise X

**Documents impactés et produits :**

| Document | Action | Statut |
|---|---|---|
| `glossaire.md` | Enrichissement complet (acronymes + termes métier) | 🟡 À valider |
| `specs/index.md` | Catalogue des 22 sous-thématiques / 37 activités | 🟡 À valider |
| `specs/processus/cycle-controle.md` | Processus PR-01 créé | 🟡 À valider |
| `specs/regles-gestion/RG-001.md` | Programmation initiale fixe | 🟡 À valider |
| `specs/regles-gestion/RG-002.md` | Programmation ajustée au fil de l'eau | 🟡 À valider |
| `specs/regles-gestion/RG-003.md` | Modulation pression de contrôle | 🟡 À valider |
| `specs/regles-gestion/RG-004.md` | Signature obligatoire des décisions | 🟡 À valider |
| `specs/regles-gestion/RG-005.md` | Habilitation pouvoir de décision | 🟡 À valider |
| `bdd/schema.md` | Schéma SQL v0.1 (10 tables, types ENUM, contraintes RG) | 🟡 À valider |
| `bdd/diagramme.md` | ERD Mermaid v0.1 | 🟡 À valider |

**Points laissés ouverts (questions aux sachants) :**
- Calcul et fréquence de mise à jour de l'indice de confiance (RG-003)
- Graduation exacte du niveau de risque (RG-003)
- Modifiabilité de la programmation initiale après validation (RG-001)
- Périmètre et temporalité des délégations de décision (RG-005)
- Impacts des décisions : automatiques ou manuels ? (RG-004)

**Prochaine session :** Choisir une sous-thématique à spécifier en détail (ex : Autorisation à produire ou Contrôle des cultures)

---

## Session 000 — 2026-04-02 — Initialisation du corpus

**Input :** Description métier initiale + choix techniques + conventions

**Décisions prises :**
- Nom du projet : `conception`
- Stack : PostgreSQL + FastAPI
- Wiki : MkDocs + Material theme
- Conventions de nommage posées

**Documents créés :**
- Structure complète du corpus (`CLAUDE.md`, `mkdocs.yml`, `docs/`)
- `glossaire.md` v0.1 (termes de base)
- `conventions.md` v0.1 (conventions PostgreSQL + FastAPI)
