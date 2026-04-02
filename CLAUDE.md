# CLAUDE.md — Instructions permanentes pour ce projet

## Contexte
Refonte du SI métier d'Entreprise X (contrôle officiel des semences et plants, domaine GNIS).
Stack : PostgreSQL + FastAPI. Documentation wiki via MkDocs + Material.

## Règle fondamentale : cohérence inter-documents

**À chaque modification d'un document, TOUJOURS vérifier et mettre à jour si nécessaire :**

| Document modifié | Vérifier obligatoirement |
|---|---|
| `glossaire.md` | Tous les documents qui utilisent le terme |
| `conventions.md` | Schéma SQL, OpenAPI, tous les noms d'entités |
| `specs/processus/*.md` | Règles de gestion liées, schéma SQL, endpoints OpenAPI, scénarios de test |
| `specs/regles-gestion/RG-*.md` | Spec processus parent, colonnes SQL concernées, description endpoint OpenAPI, scénarios de test |
| `bdd/schema.sql` | ERD Mermaid (`bdd/diagramme.mermaid`), données de test (`bdd/donnees-test.sql`), OpenAPI (types de retour) |
| `api/openapi.yaml` | Scénarios de test, spec processus liés |
| `tests/*.md` | Spec processus parent, règles de gestion testées |

**Aucun fichier ne doit jamais être mis à jour de façon isolée.**

## Vérification de cohérence — checklist obligatoire

Avant de livrer des fichiers mis à jour, répondre explicitement à ces questions :

1. Les termes utilisés sont-ils tous définis dans `glossaire.md` ?
2. Les noms de tables, colonnes, endpoints respectent-ils `conventions.md` ?
3. Chaque règle de gestion modifiée est-elle tracée dans : spec + SQL (commentaire) + OpenAPI (description) + test ?
4. Le `journal-iterations.md` est-il mis à jour avec la session courante ?
5. Le statut front matter des documents modifiés est-il passé à `a_valider` ?
6. Le sommaire `index.md` concerné est-il à jour ?

## Workflow de session

1. Input métier fourni par l'utilisateur
2. Analyse d'impact présentée AVANT toute modification
3. Validation du périmètre d'impact par l'utilisateur
4. Production des fichiers mis à jour
5. Relecture et validation utilisateur → passage en statut `valide`

## Statuts des documents

- `a_valider` : modifié en session, en attente de relecture métier
- `valide` : relu et approuvé par les sachants
- `archive` : obsolète, conservé pour historique

## Conventions de nommage (résumé)

- Tables PostgreSQL : `snake_case` singulier (`demande_autorisation`)
- Colonnes : `snake_case` (`date_creation`, `id_operateur`)
- Clés primaires : `id UUID DEFAULT gen_random_uuid()`
- Clés étrangères : `id_<table_cible>`
- Index : `idx_<table>_<colonne>`
- Endpoints API : `kebab-case` pluriel sous `/api/v1/`
- Schémas Pydantic : `PascalCase` + suffixe (`DemandeAutorisationCreate`)
- Règles de gestion : `RG-XXX`
- Cas de test : `CT-XXX`
- Statuts : underscore minuscules (`a_valider`, `en_cours`)
