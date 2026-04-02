# SI Semences — Documentation de conception

Bienvenue sur le wiki de conception du SI métier d'Entreprise X,
dédié au contrôle officiel des semences et plants.

## Navigation rapide

| Section | Description |
|---|---|
| [Glossaire](glossaire.md) | Définitions des termes métier |
| [Conventions](conventions.md) | Règles de nommage BDD, API, docs |
| [Spécifications](specs/index.md) | Processus fonctionnels et règles de gestion |
| [Base de données](bdd/schema.md) | Schéma SQL et diagramme ERD |
| [API](api/index.md) | Spécification OpenAPI |
| [Tests](tests/index.md) | Scénarios de test fonctionnels |
| [Guide utilisateur](guide-utilisateur/index.md) | Manuel utilisateur |
| [Journal des itérations](journal-iterations.md) | Historique des sessions |

## Statut des documents

!!! info "Légende des statuts"
    - 🟡 **À valider** — document modifié en session, en attente de relecture métier
    - 🟢 **Validé** — relu et approuvé par les sachants
    - ⚫ **Archivé** — obsolète, conservé pour historique

## Périmètre du projet

Le SI couvre les **4 thématiques de contrôle officiel** :

1. **Surveillance phytosanitaire** — passeports phytosanitaires, PGRP, certificats export
2. **Autorisation à produire** — enregistrement opérateurs, agréments personnel et laboratoires
3. **Surveillance semences et plants** — cultures, lots, laboratoires, personnels
4. **Référentiels professionnels** — PQP/ESTA, GSPP, Label Rouge, Végétal local
