# Product Backlog — EduTutor IA · APOCAL'IPSSI 2026

> **Projet :** EduTutor IA  
> **Équipe :** Équipe 10  
> **Dernière mise à jour :** J1  
> **Planning :** S0 cadrage (lundi matin) · S1–S7 (lundi après-midi → jeudi après-midi)  
> **1 sprint = une demi-journée**

---

## Périmètre des releases

| Release | Contenu | Statut |
|---------|---------|--------|
| **R1 – MVP** | US-01 à US-10 · Parcours étudiant complet (F1-F6) + intégration minimale enseignante (Mme Lefèvre) | En cours |
| **R2 – Évolutions** | US-11 à US-13 · Flashcards, résumé IA, questions ouvertes | Backlog |

---

## Backlog

| ID | Epic | User Story | MoSCoW | SP | Sprint | Release | Definition of Ready | Definition of Done |
|----|------|-----------|--------|----|--------|---------|--------------------|--------------------|
| US-01 | Authentification | En tant qu'**étudiant**, je veux **créer un compte** afin d'**accéder à EduTutor IA**. | MUST | 3 | S1 | R1 | Maquettes validées | Compte créé + email validé |
| US-02 | Authentification | En tant qu'**étudiant**, je veux **me connecter** afin d'**accéder à mes quiz**. | MUST | 2 | S1 | R1 | API auth disponible | Connexion fonctionnelle |
| US-03 | Cours | En tant qu'**étudiant**, je veux **importer un PDF ou saisir un texte** afin de **créer un quiz**. | MUST | 5 | S2 | R1 | Règles PDF ≤ 5 Mo et texte ≥ 200 caractères définies | PDF/Texte accepté et validé |
| US-04 | Quiz | En tant qu'**étudiant**, je veux **générer 10 QCM** afin de **réviser**. | MUST | 8 | S3 | R1 | LLM local configuré | 10 QCM générés avec 4 réponses et 1 bonne réponse |
| US-05 | Quiz | En tant qu'**étudiant**, je veux **répondre au quiz** afin d'**évaluer mes connaissances**. | MUST | 5 | S4 | R1 | Questions disponibles | Réponses enregistrées et correction automatique |
| US-06 | Résultats | En tant qu'**étudiant**, je veux **voir mon score** afin d'**identifier mes lacunes**. | MUST | 3 | S4 | R1 | Correction terminée | Score /10 + détail bonnes/mauvaises réponses affiché |
| US-07 | Historique | En tant qu'**étudiant**, je veux **consulter mes anciens quiz** afin de **suivre ma progression**. | MUST | 5 | S5 | R1 | Modèles Quiz/Question persistés | Historique par utilisateur affiché avec date, cours, score |
| US-08 | Suivi enseignant | En tant qu'**enseignante**, je veux **consulter les scores de mes étudiants** afin d'**identifier les décrocheurs**. | SHOULD | 5 | S6 | R1 | Historique étudiant disponible | Vue enseignant affichant les scores des 28 étudiants |
| US-09 | Suivi enseignant | En tant qu'**enseignante**, je veux **filtrer les étudiants en difficulté** afin d'**adapter mon accompagnement**. | SHOULD | 3 | S6 | R1 | Scores disponibles | Filtre étudiants à risque opérationnel |
| US-10 | Suivi enseignant | En tant qu'**enseignante**, je veux **envoyer des conseils personnalisés** afin d'**accompagner mes étudiants**. | SHOULD | 5 | S7 | R1 | Vue enseignant disponible | Conseil envoyé ou préparé depuis l'interface |
| US-11 | Flashcards | En tant qu'**étudiant**, je veux **générer des flashcards** afin de **diversifier mes révisions**. | COULD | 8 | — | R2 | Quiz disponible | Flashcards générées |
| US-12 | Résumé IA | En tant qu'**étudiant**, je veux **obtenir un résumé automatique** afin de **réviser rapidement**. | COULD | 5 | — | R2 | LLM disponible | Résumé généré |
| US-13 | Questions ouvertes | En tant qu'**enseignante**, je veux **générer des questions ouvertes** afin d'**enrichir mes évaluations**. | COULD | 8 | — | R2 | LLM disponible | Questions ouvertes générées |

---

## Vélocité cible par sprint

| Sprint | Demi-journée | Stories | SP |
|--------|--------------|---------|----|
| S0 | Lundi matin | Cadrage — pas de dev | — |
| S1 | Lundi après-midi | US-01, US-02 | 5 |
| S2 | Mardi matin | US-03 | 5 |
| S3 | Mardi après-midi | US-04 | 8 |
| S4 | Mercredi matin | US-05, US-06 | 8 |
| S5 | Mercredi après-midi | US-07 | 5 |
| S6 | Jeudi matin | US-08, US-09 | 8 |
| S7 | Jeudi après-midi | US-10 | 5 |
| **Total R1** | | | **44 SP** |

---

## Décision J1 – MoSCoW

La cible enseignante est intégrée en **SHOULD** dans la Release 1. Justification : les fonctionnalités enseignantes apportent une forte valeur pédagogique mais ne doivent pas compromettre le MVP étudiant F1-F6. Les stories US-08 à US-10 réutilisent l'historique, les scores et les données déjà produites par le parcours étudiant. Elles sont donc ajoutées en fin de Release 1, sur les sprints S6 et S7, après sécurisation du cœur MVP. Les fonctionnalités plus avancées comme flashcards, résumé automatique et questions ouvertes restent en Release 2.

---

## Personas de référence

| Persona | Rôle | Contexte |
|---------|------|---------|
| **Étudiant type** | Utilisateur principal | Étudiant du supérieur en révision autonome |
| **Mme Sophie Lefèvre** | Enseignante BTS Communication — Lyon | 42 ans · 28 étudiants · veut suivre les scores et accompagner les décrocheurs |
