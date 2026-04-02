---
titre: Schéma SQL — Base de données
statut: a_valider
version: 0.1
derniere_modification: 2026-04-02
modifie_par: session-001
resume_modifications: |
  Création initiale depuis description.md :
  - Entités du cycle de contrôle (PR-01)
  - Types ENUM des statuts métier
  - Contraintes issues de RG-001 à RG-005
---

# Schéma SQL

!!! warning "Statut : À valider"
    Ce schéma couvre uniquement le cycle de contrôle (PR-01). Il sera enrichi à chaque session.

## Types ENUM

```sql
-- Statuts du dossier/demande
CREATE TYPE dossier_statut AS ENUM (
    'brouillon',
    'soumis',
    'en_instruction',
    'decision_rendue',
    'archive'
);

-- Statuts d'un contrôle
CREATE TYPE controle_statut AS ENUM (
    'programme',
    'planifie',
    'en_cours',
    'realise',
    'annule'
);

-- Statuts d'un agrément
CREATE TYPE agrement_statut AS ENUM (
    'en_attente',
    'accorde',
    'refuse',
    'suspendu',
    'retire'
);

-- Types de programmation
CREATE TYPE programmation_type AS ENUM (
    'initiale',
    'ajustee'
);

-- Types de décision
CREATE TYPE decision_type AS ENUM (
    'favorable',
    'defavorable',
    'avec_reserve',
    'sans_suite'
);
```

## Tables

### utilisateur

```sql
-- Collaborateurs Entreprise X (inspecteurs, agents admin, référents, directrice)
CREATE TABLE utilisateur (
    id                  UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    nom                 VARCHAR(100) NOT NULL,
    prenom              VARCHAR(100) NOT NULL,
    email               VARCHAR(255) NOT NULL,
    role                VARCHAR(50)  NOT NULL,  -- 'inspecteur', 'agent_administratif', etc.
    id_pole_antenne     UUID REFERENCES pole_antenne(id),
    est_actif           BOOLEAN DEFAULT TRUE,
    created_at          TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at          TIMESTAMP WITH TIME ZONE,
    deleted_at          TIMESTAMP WITH TIME ZONE,
    CONSTRAINT uq_utilisateur_email UNIQUE (email)
);

CREATE INDEX idx_utilisateur_role ON utilisateur(role);
CREATE INDEX idx_utilisateur_pole_antenne ON utilisateur(id_pole_antenne);
```

### pole_antenne

```sql
-- Les 3 pôles centraux et 6 antennes régionales de la DQ
CREATE TABLE pole_antenne (
    id          UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    code        VARCHAR(20)  NOT NULL,
    libelle     VARCHAR(200) NOT NULL,
    type        VARCHAR(20)  NOT NULL CHECK (type IN ('pole', 'antenne')),
    region      VARCHAR(100),
    created_at  TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at  TIMESTAMP WITH TIME ZONE,
    CONSTRAINT uq_pole_antenne_code UNIQUE (code)
);
```

### operateur

```sql
-- Personnes morales du secteur du produit X
-- RG-003 : porte l'indice de confiance
CREATE TABLE operateur (
    id                  UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    siret               VARCHAR(14)     NOT NULL,
    raison_sociale      VARCHAR(500)    NOT NULL,
    adresse             TEXT,
    code_postal         VARCHAR(10),
    commune             VARCHAR(200),
    indice_confiance    NUMERIC(3,2)    DEFAULT 1.00
                            CHECK (indice_confiance BETWEEN 0.00 AND 1.00),
    est_actif           BOOLEAN DEFAULT TRUE,
    created_at          TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at          TIMESTAMP WITH TIME ZONE,
    deleted_at          TIMESTAMP WITH TIME ZONE,
    CONSTRAINT uq_operateur_siret UNIQUE (siret)
);

CREATE INDEX idx_operateur_siret ON operateur(siret);
CREATE INDEX idx_operateur_indice_confiance ON operateur(indice_confiance);
```

### plan_controle

```sql
-- Plan de contrôle annuel issu du Plan de performance
CREATE TABLE plan_controle (
    id              UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    annee           SMALLINT    NOT NULL CHECK (annee BETWEEN 2000 AND 2100),
    libelle         VARCHAR(500) NOT NULL,
    statut          VARCHAR(50) DEFAULT 'en_preparation',
    date_validation DATE,
    id_validateur   UUID REFERENCES utilisateur(id),
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at      TIMESTAMP WITH TIME ZONE,
    CONSTRAINT uq_plan_controle_annee UNIQUE (annee)
);
```

### programmation

```sql
-- Déclinaison opérationnelle du plan de contrôle par région
-- RG-001 : la programmation initiale est fixe
-- RG-002 : la programmation ajustée référence une initiale parente
CREATE TABLE programmation (
    id                          UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    id_plan_controle            UUID NOT NULL REFERENCES plan_controle(id),
    id_pole_antenne             UUID NOT NULL REFERENCES pole_antenne(id),
    type_programmation          programmation_type NOT NULL,
    date_gel                    DATE,
    id_programmation_initiale   UUID REFERENCES programmation(id),
    created_at                  TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at                  TIMESTAMP WITH TIME ZONE,
    -- RG-001 : si initiale, date_gel obligatoire
    CONSTRAINT ck_programmation_initiale_gel
        CHECK (type_programmation != 'initiale' OR date_gel IS NOT NULL),
    -- RG-002 : si ajustée, référence une initiale
    CONSTRAINT ck_programmation_ajustee_parente
        CHECK (type_programmation = 'initiale' OR id_programmation_initiale IS NOT NULL)
);

CREATE INDEX idx_programmation_plan ON programmation(id_plan_controle);
CREATE INDEX idx_programmation_antenne ON programmation(id_pole_antenne);
```

### ordre_controle

```sql
-- Ordre de contrôle émis lors de l'ordonnancement
CREATE TABLE ordre_controle (
    id                  UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    reference           VARCHAR(50)  NOT NULL,
    id_programmation    UUID         NOT NULL REFERENCES programmation(id),
    id_operateur        UUID         NOT NULL REFERENCES operateur(id),
    type_activite       VARCHAR(100) NOT NULL,  -- ex: 'controle_cultures', 'agrement_labo'
    statut              controle_statut DEFAULT 'programme',
    date_emission       DATE         NOT NULL DEFAULT CURRENT_DATE,
    date_planifiee      DATE,
    id_affecte_a        UUID         REFERENCES utilisateur(id),
    created_at          TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at          TIMESTAMP WITH TIME ZONE,
    CONSTRAINT uq_ordre_controle_reference UNIQUE (reference)
);

CREATE INDEX idx_ordre_controle_operateur ON ordre_controle(id_operateur);
CREATE INDEX idx_ordre_controle_statut ON ordre_controle(statut);
CREATE INDEX idx_ordre_controle_affecte ON ordre_controle(id_affecte_a);
```

### controle

```sql
-- Réalisation effective d'un contrôle
CREATE TABLE controle (
    id                  UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    id_ordre_controle   UUID NOT NULL REFERENCES ordre_controle(id),
    id_inspecteur       UUID NOT NULL REFERENCES utilisateur(id),
    statut              controle_statut DEFAULT 'en_cours',
    date_debut          DATE,
    date_fin            DATE,
    created_at          TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at          TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_controle_ordre ON controle(id_ordre_controle);
CREATE INDEX idx_controle_inspecteur ON controle(id_inspecteur);
```

### point_controle

```sql
-- Points de contrôle qualifiés lors d'un contrôle
CREATE TABLE point_controle (
    id              UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    id_controle     UUID NOT NULL REFERENCES controle(id),
    libelle         VARCHAR(500) NOT NULL,
    resultat        VARCHAR(50) CHECK (resultat IN ('conforme', 'non_conforme', 'sans_objet')),
    commentaire     TEXT,
    id_qualifie_par UUID REFERENCES utilisateur(id),
    date_qualification TIMESTAMP WITH TIME ZONE,
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at      TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_point_controle_controle ON point_controle(id_controle);
```

### rapport

```sql
-- Rapport d'évaluation ou constat produit à l'issue du contrôle
CREATE TABLE rapport (
    id                  UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    id_controle         UUID NOT NULL REFERENCES controle(id),
    id_redacteur        UUID NOT NULL REFERENCES utilisateur(id),
    id_reviseur         UUID REFERENCES utilisateur(id),  -- référent technique régional
    contenu             TEXT,
    date_redaction      DATE,
    date_revision       DATE,
    statut              VARCHAR(50) DEFAULT 'brouillon'
                            CHECK (statut IN ('brouillon', 'en_revision', 'valide')),
    created_at          TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at          TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_rapport_controle ON rapport(id_controle);
```

### decision

```sql
-- Décision administrative finale
-- RG-004 : signature obligatoire
CREATE TABLE decision (
    id                  UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    id_rapport          UUID NOT NULL REFERENCES rapport(id),
    id_operateur        UUID NOT NULL REFERENCES operateur(id),
    type_decision       decision_type NOT NULL,
    statut              VARCHAR(50) DEFAULT 'en_preparation'
                            CHECK (statut IN ('en_preparation', 'proposee', 'rendue', 'annulee')),
    id_signataire       UUID REFERENCES utilisateur(id),
    date_signature      DATE,
    date_notification   DATE,
    commentaire         TEXT,
    created_at          TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at          TIMESTAMP WITH TIME ZONE,
    -- RG-004 : décision rendue = signature obligatoire
    CONSTRAINT ck_decision_signee
        CHECK (statut != 'rendue' OR (id_signataire IS NOT NULL AND date_signature IS NOT NULL))
);

CREATE INDEX idx_decision_operateur ON decision(id_operateur);
CREATE INDEX idx_decision_statut ON decision(statut);
```

### habilitation_decision

```sql
-- Délégations du pouvoir de décision — RG-005
CREATE TABLE habilitation_decision (
    id              UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    id_utilisateur  UUID NOT NULL REFERENCES utilisateur(id),
    type_activite   VARCHAR(100),  -- NULL = toutes activités
    date_debut      DATE NOT NULL,
    date_fin        DATE,
    accordee_par    UUID NOT NULL REFERENCES utilisateur(id),
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at      TIMESTAMP WITH TIME ZONE,
    CONSTRAINT ck_habilitation_dates
        CHECK (date_fin IS NULL OR date_fin > date_debut)
);

CREATE INDEX idx_habilitation_utilisateur ON habilitation_decision(id_utilisateur);
```

### niveau_risque_situation

```sql
-- Niveaux de risque par zone/espèce — RG-003
CREATE TABLE niveau_risque_situation (
    id                  UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    zone_geographique   VARCHAR(100),
    groupe_espece       VARCHAR(100),
    niveau_risque       SMALLINT NOT NULL CHECK (niveau_risque BETWEEN 1 AND 5),
    commentaire         TEXT,
    created_at          TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at          TIMESTAMP WITH TIME ZONE
);
```
