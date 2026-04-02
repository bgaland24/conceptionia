---
titre: Conventions de nommage
statut: a_valider
version: 0.1
derniere_modification: 2026-04-02
modifie_par: session-000
resume_modifications: |
  Création initiale — conventions PostgreSQL + FastAPI
---

# Conventions de nommage

!!! warning "Statut : À valider"
    Ces conventions doivent être validées avant le démarrage de la session 1.
    Toute exception doit être documentée ici.

## Base de données (PostgreSQL)

### Tables

- Format : `snake_case` **singulier**
- Exemples : `operateur`, `demande_autorisation`, `ordre_controle`, `lot_semence`

### Colonnes

- Format : `snake_case`
- Clé primaire : toujours `id UUID DEFAULT gen_random_uuid()`
- Clé étrangère : `id_<table_cible>` (ex : `id_operateur`, `id_inspecteur`)
- Timestamps systématiques : `created_at TIMESTAMP WITH TIME ZONE DEFAULT now()` et `updated_at TIMESTAMP WITH TIME ZONE`
- Soft delete : `deleted_at TIMESTAMP WITH TIME ZONE` (NULL = actif)
- Colonnes booléennes : préfixe `est_` ou `a_` (ex : `est_actif`, `a_agrément`)

### Nommage des objets PostgreSQL

| Objet | Format | Exemple |
|---|---|---|
| Index | `idx_<table>_<colonne>` | `idx_operateur_siret` |
| Contrainte CHECK | `ck_<table>_<règle>` | `ck_dossier_statut_valide` |
| Contrainte UNIQUE | `uq_<table>_<colonne>` | `uq_operateur_siret` |
| Clé étrangère | `fk_<table>_<table_cible>` | `fk_dossier_operateur` |
| Séquence | `seq_<table>_<colonne>` | (éviter, préférer UUID) |
| Type ENUM | `<domaine>_statut` ou `<domaine>_type` | `dossier_statut`, `controle_type` |

### Statuts métier (valeurs d'ENUM)

```sql
-- Statuts dossier
CREATE TYPE dossier_statut AS ENUM (
    'brouillon',
    'soumis',
    'en_instruction',
    'decision_rendue',
    'archive'
);

-- Statuts contrôle
CREATE TYPE controle_statut AS ENUM (
    'programme',
    'planifie',
    'en_cours',
    'realise',
    'annule'
);

-- Statuts agrément
CREATE TYPE agrement_statut AS ENUM (
    'en_attente',
    'accorde',
    'refuse',
    'suspendu',
    'retire'
);
```

---

## API (FastAPI / OpenAPI)

### URLs

- Format des ressources : `kebab-case` **pluriel**
- Préfixe obligatoire : `/api/v1/`
- Exemples :
  - `/api/v1/demandes-autorisation`
  - `/api/v1/ordres-controle`
  - `/api/v1/operateurs/{id}/lots-semences`

### Paramètres

- Query params : `snake_case` (ex : `?statut_dossier=en_instruction&id_operateur=...`)
- Path params : `snake_case` (ex : `/{id_dossier}`)

### Verbes HTTP

| Action | Verbe | Code succès |
|---|---|---|
| Lister | `GET` | `200` |
| Lire un élément | `GET` | `200` |
| Créer | `POST` | `201` |
| Remplacer entièrement | `PUT` | `200` |
| Modifier partiellement | `PATCH` | `200` |
| Supprimer | `DELETE` | `204` |

### Codes d'erreur standard

| Code | Usage |
|---|---|
| `400` | Requête malformée |
| `401` | Non authentifié |
| `403` | Non autorisé |
| `404` | Ressource introuvable |
| `409` | Conflit (doublon) |
| `422` | Erreur de validation (FastAPI natif) |
| `500` | Erreur serveur |

### Schémas Pydantic

- Format : `PascalCase` + suffixe fonctionnel

| Suffixe | Usage |
|---|---|
| `Create` | Corps d'une requête POST |
| `Update` | Corps d'une requête PATCH |
| `Read` | Réponse retournée par l'API |
| `List` | Réponse liste paginée |

Exemples : `DemandeAutorisationCreate`, `OperateurRead`, `OrdreControleList`

### Tags OpenAPI (regroupement par domaine)

- `Phytosanitaire`
- `Autorisation`
- `Surveillance`
- `Referentiels`
- `Operateurs`
- `Administration`

---

## Documentation

### Fichiers

- Format : `kebab-case` avec extension `.md`
- Exemples : `demande-autorisation.md`, `controle-cultures.md`

### Codes de référence

| Code | Format | Série | Exemple |
|---|---|---|---|
| Règle de gestion | `RG-XXX` | 001–999 | `RG-001` |
| Cas de test | `CT-XXX` | 001–999 | `CT-001` |
| Processus | `PR-XX` | 01–99 | `PR-01` |

### Front matter des documents de spec

```yaml
---
titre: <titre humain>
statut: a_valider        # ou "valide" ou "archive"
version: 1.0
derniere_modification: YYYY-MM-DD
modifie_par: session-XXX
resume_modifications: |
  Description des changements apportés lors de cette session
---
```

---

## Exceptions documentées

*Aucune exception pour l'instant. Toute dérogation aux conventions ci-dessus doit être justifiée et listée ici.*
