# J4 — Analyse de risques

> **Projet :** EduTutor IA · **Équipe :** Équipe 10 · **Perturbation :** J4
> Couvre **CA-J4-3** (≥ 5 risques en matrice probabilité × impact) et **CA-J4-4**
> (chaque risque prioritaire a une action préventive **estimée** et priorisée au backlog).

---

## 1. Échelles

**Probabilité (P)** : 1 = Rare · 2 = Peu probable · 3 = Possible · 4 = Probable · 5 = Quasi certain
**Impact (I)** : 1 = Négligeable · 2 = Mineur · 3 = Modéré · 4 = Majeur · 5 = Critique
**Criticité = P × I** — Seuil d'action prioritaire : **criticité ≥ 9** (🔴).

---

## 2. Registre des risques

| ID | Risque | Axe | P | I | Criticité | Niveau |
|----|--------|-----|---|---|-----------|--------|
| **R1** | Serveurs saturés au pic national → service indisponible | 📈 scale | 4 | 5 | **20** | 🔴 |
| **R2** | Non-conformité RGAA → rejet du marché public (État) | ♿ a11y | 3 | 5 | **15** | 🔴 |
| **R3** | Le LLM local (Ollama) devient le goulot d'étranglement sous charge | 📈 scale | 4 | 4 | **16** | 🔴 |
| **R4** | Traductions incomplètes / LLM répond dans la mauvaise langue | 🌍 i18n | 3 | 3 | **9** | 🔴 |
| **R5** | Refonte scale/i18n dans la panique casse le MVP livré (F1-F6) | 📈 qualité | 3 | 4 | **12** | 🔴 |
| **R6** | Sortie de données hors UE lors de la montée en charge (RGPD) | 🔒 RGPD | 2 | 5 | **10** | 🔴 |
| **R7** | Coût infra (autoscaling) explose sans budget maîtrisé | 📈 coût | 3 | 2 | 6 | 🟠 |

---

## 3. Matrice Probabilité × Impact

| P \ I | 1 | 2 | 3 | 4 | 5 |
|-------|---|---|---|---|---|
| **5 (quasi certain)** | | | | | **R1** 🔴 |
| **4 (probable)** | | | | **R3** 🔴 | |
| **3 (possible)** | | R7 🟠 | **R4** 🔴 | **R5** 🔴 | **R2** 🔴 |
| **2 (peu probable)** | | | | | **R6** 🔴 |
| **1 (rare)** | | | | | |

> Zone rouge (criticité ≥ 9) : R1, R2, R3, R4, R5, R6 → **actions préventives obligatoires**.
> Zone orange : R7 → surveillance.

---

## 4. Actions préventives (→ backlog `doc_livrable/Jeudi/Artefact_5_Product_Backlog_V4_J4.xlsx`)

Chaque risque prioritaire reçoit une action **préventive** (réduit P ou I), **estimée en SP** et
tracée dans le backlog J4 (stories **US-21 → US-26**, après les IDs déjà pris par J3 et J3-bis).

| Risque | Action préventive | Effet visé | SP | Item backlog | MoSCoW |
|--------|-------------------|-----------|----|--------------|--------|
| **R1** | Test de charge + **cache** des quiz + **autoscaling** horizontal | P 4→2 | 13 | **US-24** | MUST |
| **R2** | **Audit RGAA** + focus visible, contrastes, alt/aria, navigation clavier | P 3→1 | 8 | **US-21** | MUST |
| **R3** | **Cache** de génération + fournisseur de secours (anti-goulot LLM) | I 4→3 | 13 / 5 | **US-24, US-25** | MUST/COULD |
| **R4** | **Externalisation des textes** + **param langue LLM** + tests i18n | P 3→2 | 8 + 5 | **US-22, US-23** | MUST/SHOULD |
| **R5** | Évolutions **feature-flaggées** + non-régression F1-F6 avant merge | I 4→2 | 3 | **US-26** | MUST |
| **R6** | **Fournisseur LLM de secours 100 % local** (jamais d'appel hors UE) | P 2→1 | 5 | **US-25** | COULD |
| **R7** | Plafond de dépense + alertes coût, autoscaling borné (min/max) | I 2→1 | (inclus US-24) | US-24 | MUST |

> **IDs sans collision** : J3 occupait US-14/15/16 (sécurité), J3-bis US-17/18/19/20 (RGPD/SAR).
> J4 démarre donc à **US-21**.
