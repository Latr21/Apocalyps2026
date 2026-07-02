# Perturbation J4 — Passage à l'échelle (Pilotage)

> **Projet :** EduTutor IA · **Équipe :** Équipe 10
> **Perturbation :** J4 (jeudi) — Scalabilité · Accessibilité RGAA · Internationalisation (i18n)

Le succès national impose 3 axes. Le cœur du livrable est **managérial** : artefacts mis à jour,
analyse de risques et pilotage par courbes. La mise en œuvre technique des 3 axes est un **bonus**.

## Où sont les livrables J4

Conformément à la convention de l'équipe (un dossier par jour : `Mercredi/` pour J3/J3-bis), les
**artefacts pivotés** sont versionnés dans **`doc_livrable/Jeudi/`**. Le **pilotage spécifique J4**
(risques + courbes) est ici en `.md`.

### Artefacts mis à jour → `doc_livrable/Jeudi/`
| Artefact | Fichier J4 | Basé sur | Ajout J4 |
|----------|-----------|----------|----------|
| Vision Board | `Artefact_1_Product_Vision_Board_V2_J4.docx` | V1 | 3 axes dans vision/besoins/produit/objectifs |
| Personas | `Artefact_2_Personas_V2_J4.docx` | V1+perturbation | Persona **Lucia** (internationale + handicap) |
| Story Map | `Artefact_4_Story_Map_V3_J4.xlsx` | V2_J3 | Activité « Passer à l'échelle (J4) » + feuille Décision J4 |
| Product Backlog | `Artefact_5_Product_Backlog_V4_J4.xlsx` | **V3_J3bis** | US-21→US-26 + feuille Décision J4 |
| Release Planning | `Artefact_6_Release_Planning_V4_J4.xlsx` | **V3_J3bis** | Sprints S8/S9/R2+ + feuille Décision J4 |
| Sprint Backlog | `Artefact_7_Sprint_Backlog_V4_J4.xlsx` | **V3_J3bis** | Next sprint S8 + feuille Décision J4 |

> ⚠️ Les IDs de stories tiennent compte de l'existant : J3 avait pris US-14/15/16 (sécurité) et
> J3-bis US-17/18/19/20 (RGPD/SAR). **J4 démarre donc à US-21.**

### Pilotage J4 → `docs/pilotage/` (ce dossier)
| Fichier | Contenu | Critères |
|---------|---------|----------|
| [01-analyse-risques.md](01-analyse-risques.md) | ≥ 5 risques, matrice proba × impact, actions préventives | CA-J4-3, CA-J4-4 |
| [02-burndown-burnup.md](02-burndown-burnup.md) | Burndown (sprint S8) + burnup (projet) | CA-J4-7 |

## Suivi des critères d'acceptation
| # | Critère | Preuve |
|---|---------|--------|
| CA-J4-1 | Vision board & story map intègrent les 3 axes | `Artefact_1_..._V2_J4.docx`, `Artefact_4_..._V3_J4.xlsx` |
| CA-J4-2 | Persona élargie (international / handicap) | `Artefact_2_..._V2_J4.docx` (Lucia) |
| CA-J4-3 | ≥ 5 risques en matrice probabilité × impact | `01-analyse-risques.md` |
| CA-J4-4 | Chaque risque prioritaire a une action préventive estimée au backlog | `01-analyse-risques.md` + `Artefact_5_..._V4_J4.xlsx` |
| CA-J4-5 | Backlog repriorisé (MoSCoW) + release planning à jour | `Artefact_5_..._V4_J4.xlsx`, `Artefact_6_..._V4_J4.xlsx` |
| CA-J4-6 | Sprints précédents conservés + next sprint préparé | `Artefact_7_..._V4_J4.xlsx` (S1-S7 intacts, S8 ajouté) |
| CA-J4-7 | Burndown + burnup montrant l'impact des perturbations | `02-burndown-burnup.md` |

> **Rien de l'existant n'est écrasé** : les fichiers de `Mercredi/` (V3_J3bis) et de `artefacts/`
> restent intacts ; J4 crée de nouveaux fichiers dans `Jeudi/`.
