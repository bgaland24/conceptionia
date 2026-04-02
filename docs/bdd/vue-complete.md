---
titre: Vue complète de la base de données
statut: a_valider
version: 0.1
derniere_modification: 2026-04-02
modifie_par: session-001
---

# Base de données — Vue complète

Détail de chaque table : colonnes, types, contraintes et règles de gestion associées.

---

## pole_antenne

> Les 3 pôles centraux et 6 antennes régionales de la DQ.

| Colonne | Type | Contraintes | Description |
|---|---|---|---|
| `id` | UUID | PK | Identifiant unique |
| `code` | VARCHAR(20) | NOT NULL, UNIQUE | Code court (ex : `ANT-IDF`) |
| `libelle` | VARCHAR(200) | NOT NULL | Nom complet |
| `type` | VARCHAR(20) | NOT NULL, IN ('pole','antenne') | Nature de l'entité |
| `region` | VARCHAR(100) | — | Région couverte (antennes) |
| `created_at` | TIMESTAMPTZ | DEFAULT now() | Date de création |
| `updated_at` | TIMESTAMPTZ | — | Date de dernière modification |

---

## utilisateur

> Collaborateurs Entreprise X intervenant dans le cycle de contrôle.

| Colonne | Type | Contraintes | Description |
|---|---|---|---|
| `id` | UUID | PK | Identifiant unique |
| `nom` | VARCHAR(100) | NOT NULL | Nom de famille |
| `prenom` | VARCHAR(100) | NOT NULL | Prénom |
| `email` | VARCHAR(255) | NOT NULL, UNIQUE | Adresse email professionnelle |
| `role` | VARCHAR(50) | NOT NULL | Rôle fonctionnel |
| `id_pole_antenne` | UUID | FK → pole_antenne | Rattachement organisationnel |
| `est_actif` | BOOLEAN | DEFAULT TRUE | Compte actif ou désactivé |
| `created_at` | TIMESTAMPTZ | DEFAULT now() | — |
| `updated_at` | TIMESTAMPTZ | — | — |
| `deleted_at` | TIMESTAMPTZ | — | Soft delete |

**Valeurs de `role` :** `inspecteur` · `agent_administratif` · `referent_technique_regional` · `referent_technique_national` · `directrice_dq`

---

## operateur

> Personne morale de la filière semences et plants.

| Colonne | Type | Contraintes | Description |
|---|---|---|---|
| `id` | UUID | PK | Identifiant unique |
| `siret` | VARCHAR(14) | NOT NULL, UNIQUE | Numéro SIRET |
| `raison_sociale` | VARCHAR(500) | NOT NULL | Dénomination sociale |
| `adresse` | TEXT | — | Adresse postale |
| `code_postal` | VARCHAR(10) | — | — |
| `commune` | VARCHAR(200) | — | — |
| `indice_confiance` | NUMERIC(3,2) | DEFAULT 1.00, BETWEEN 0.00 AND 1.00 | Historique de conformité — **[RG-003](../specs/regles-gestion/RG-003.md)** |
| `est_actif` | BOOLEAN | DEFAULT TRUE | — |
| `created_at` | TIMESTAMPTZ | DEFAULT now() | — |
| `updated_at` | TIMESTAMPTZ | — | — |
| `deleted_at` | TIMESTAMPTZ | — | Soft delete |

---

## plan_controle

> Plan de contrôle annuel issu du COP.

| Colonne | Type | Contraintes | Description |
|---|---|---|---|
| `id` | UUID | PK | Identifiant unique |
| `annee` | SMALLINT | NOT NULL, UNIQUE, 2000–2100 | Année du plan |
| `libelle` | VARCHAR(500) | NOT NULL | Intitulé |
| `statut` | VARCHAR(50) | DEFAULT 'en_preparation' | État du plan |
| `date_validation` | DATE | — | Date de validation officielle |
| `id_validateur` | UUID | FK → utilisateur | Agent ayant validé |
| `created_at` | TIMESTAMPTZ | DEFAULT now() | — |
| `updated_at` | TIMESTAMPTZ | — | — |

---

## programmation

> Déclinaison opérationnelle du plan de contrôle par région.

| Colonne | Type | Contraintes | Description |
|---|---|---|---|
| `id` | UUID | PK | Identifiant unique |
| `id_plan_controle` | UUID | NOT NULL, FK → plan_controle | Plan de rattachement |
| `id_pole_antenne` | UUID | NOT NULL, FK → pole_antenne | Région concernée |
| `type_programmation` | ENUM | NOT NULL, IN ('initiale','ajustee') | Nature — **[RG-001](../specs/regles-gestion/RG-001.md)**, **[RG-002](../specs/regles-gestion/RG-002.md)** |
| `date_gel` | DATE | Obligatoire si initiale | Date de gel — **[RG-001](../specs/regles-gestion/RG-001.md)** |
| `id_programmation_initiale` | UUID | FK → programmation, obligatoire si ajustée | Référence parent — **[RG-002](../specs/regles-gestion/RG-002.md)** |
| `created_at` | TIMESTAMPTZ | DEFAULT now() | — |
| `updated_at` | TIMESTAMPTZ | — | — |

---

## niveau_risque_situation

> Niveaux de risque par zone géographique / groupe d'espèce.

| Colonne | Type | Contraintes | Description |
|---|---|---|---|
| `id` | UUID | PK | Identifiant unique |
| `zone_geographique` | VARCHAR(100) | — | Zone concernée |
| `groupe_espece` | VARCHAR(100) | — | Groupe d'espèces concerné |
| `niveau_risque` | SMALLINT | NOT NULL, BETWEEN 1 AND 5 | Niveau de 1 (faible) à 5 (critique) — **[RG-003](../specs/regles-gestion/RG-003.md)** |
| `commentaire` | TEXT | — | Justification |
| `created_at` | TIMESTAMPTZ | DEFAULT now() | — |
| `updated_at` | TIMESTAMPTZ | — | — |

---

## ordre_controle

> Instruction formelle de réaliser un contrôle.

| Colonne | Type | Contraintes | Description |
|---|---|---|---|
| `id` | UUID | PK | Identifiant unique |
| `reference` | VARCHAR(50) | NOT NULL, UNIQUE | Référence lisible (ex : `OC-2026-0042`) |
| `id_programmation` | UUID | NOT NULL, FK → programmation | Programmation d'origine |
| `id_operateur` | UUID | NOT NULL, FK → operateur | Opérateur ciblé |
| `type_activite` | VARCHAR(100) | NOT NULL | Type de contrôle (ex : `controle_cultures`) |
| `statut` | ENUM | DEFAULT 'programme' | `programme` · `planifie` · `en_cours` · `realise` · `annule` |
| `date_emission` | DATE | NOT NULL, DEFAULT today | Date d'émission |
| `date_planifiee` | DATE | — | Date prévue d'intervention |
| `id_affecte_a` | UUID | FK → utilisateur | Inspecteur affecté |
| `created_at` | TIMESTAMPTZ | DEFAULT now() | — |
| `updated_at` | TIMESTAMPTZ | — | — |

---

## controle

> Réalisation effective d'un contrôle terrain.

| Colonne | Type | Contraintes | Description |
|---|---|---|---|
| `id` | UUID | PK | Identifiant unique |
| `id_ordre_controle` | UUID | NOT NULL, FK → ordre_controle | Ordre d'origine |
| `id_inspecteur` | UUID | NOT NULL, FK → utilisateur | Inspecteur ayant réalisé |
| `statut` | ENUM | DEFAULT 'en_cours' | `programme` · `planifie` · `en_cours` · `realise` · `annule` |
| `date_debut` | DATE | — | Début de l'intervention |
| `date_fin` | DATE | — | Fin de l'intervention |
| `created_at` | TIMESTAMPTZ | DEFAULT now() | — |
| `updated_at` | TIMESTAMPTZ | — | — |

---

## point_controle

> Critères vérifiés lors d'un contrôle.

| Colonne | Type | Contraintes | Description |
|---|---|---|---|
| `id` | UUID | PK | Identifiant unique |
| `id_controle` | UUID | NOT NULL, FK → controle | Contrôle parent |
| `libelle` | VARCHAR(500) | NOT NULL | Intitulé du point vérifié |
| `resultat` | VARCHAR(50) | IN ('conforme','non_conforme','sans_objet') | Résultat de la vérification |
| `commentaire` | TEXT | — | Observation libre |
| `id_qualifie_par` | UUID | FK → utilisateur | Agent ayant qualifié ce point |
| `date_qualification` | TIMESTAMPTZ | — | Date de qualification |
| `created_at` | TIMESTAMPTZ | DEFAULT now() | — |
| `updated_at` | TIMESTAMPTZ | — | — |

---

## rapport

> Constat produit à l'issue du contrôle, base de la décision.

| Colonne | Type | Contraintes | Description |
|---|---|---|---|
| `id` | UUID | PK | Identifiant unique |
| `id_controle` | UUID | NOT NULL, FK → controle | Contrôle concerné |
| `id_redacteur` | UUID | NOT NULL, FK → utilisateur | Inspecteur rédacteur |
| `id_reviseur` | UUID | FK → utilisateur | Référent technique régional (révision) |
| `contenu` | TEXT | — | Corps du rapport |
| `statut` | VARCHAR(50) | IN ('brouillon','en_revision','valide') | État du rapport |
| `date_redaction` | DATE | — | Date de rédaction |
| `date_revision` | DATE | — | Date de révision |
| `created_at` | TIMESTAMPTZ | DEFAULT now() | — |
| `updated_at` | TIMESTAMPTZ | — | — |

---

## decision

> Acte administratif final signé. — **[RG-004](../specs/regles-gestion/RG-004.md)**

| Colonne | Type | Contraintes | Description |
|---|---|---|---|
| `id` | UUID | PK | Identifiant unique |
| `id_rapport` | UUID | NOT NULL, FK → rapport | Rapport fondateur |
| `id_operateur` | UUID | NOT NULL, FK → operateur | Opérateur concerné |
| `type_decision` | ENUM | NOT NULL | `favorable` · `defavorable` · `avec_reserve` · `sans_suite` |
| `statut` | VARCHAR(50) | DEFAULT 'en_preparation' | `en_preparation` · `proposee` · `rendue` · `annulee` |
| `id_signataire` | UUID | FK → utilisateur, obligatoire si rendue | Signataire — **[RG-004](../specs/regles-gestion/RG-004.md)** |
| `date_signature` | DATE | Obligatoire si rendue | — **[RG-004](../specs/regles-gestion/RG-004.md)** |
| `date_notification` | DATE | — | Date de notification à l'opérateur |
| `commentaire` | TEXT | — | — |
| `created_at` | TIMESTAMPTZ | DEFAULT now() | — |
| `updated_at` | TIMESTAMPTZ | — | — |

---

## habilitation_decision

> Délégation du pouvoir de décision. — **[RG-005](../specs/regles-gestion/RG-005.md)**

| Colonne | Type | Contraintes | Description |
|---|---|---|---|
| `id` | UUID | PK | Identifiant unique |
| `id_utilisateur` | UUID | NOT NULL, FK → utilisateur | Bénéficiaire de la délégation |
| `type_activite` | VARCHAR(100) | — | Périmètre (NULL = toutes activités) |
| `date_debut` | DATE | NOT NULL | Début de validité |
| `date_fin` | DATE | date_fin > date_debut | Fin de validité (NULL = indéterminée) |
| `accordee_par` | UUID | NOT NULL, FK → utilisateur | Directrice DQ accordant la délégation — **[RG-005](../specs/regles-gestion/RG-005.md)** |
| `created_at` | TIMESTAMPTZ | DEFAULT now() | — |
| `updated_at` | TIMESTAMPTZ | — | — |
