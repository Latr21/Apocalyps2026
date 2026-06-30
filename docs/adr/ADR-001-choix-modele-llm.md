# ADR-001 — Choix du modèle LLM local pour la génération de quiz

**Date :** 30/06/2026
**Auteur :** Équipe EduTutor IA
**Statut :** Accepté

---

## 1. Contexte

La fonctionnalité F3 du MVP génère un quiz de 10 QCM à partir d'un cours uploadé par l'utilisateur, via un LLM appelé en local par Ollama.

Le kit impose Ollama en local (modèle par défaut : Llama 3.1 8B). Cette contrainte est liée au RGPD : la cible étant le B2B éducation, aucune donnée d'élève ou de cours ne doit sortir du serveur. Un fournisseur externe type OpenAI ferait sortir les données de l'UE, ce qui est rédhibitoire.

Problème déclencheur : avec Llama 3.1 8B, la génération d'un quiz complet est trop lente. L'utilisateur clique sur « générer » et attend bien trop longtemps. Pour un produit dont la promesse est la rapidité de révision, c'est bloquant côté expérience utilisateur. On doit réduire cette latence **sans casser la contrainte RGPD** (donc en restant en local).

## 2. Options envisagées

Benchmark reproductible : même prompt (générer 10 QCM sur un cours de référence), même machine, 5 runs par modèle. On mesure la **médiane (p50)** et le **95e percentile (p95)**, pas la moyenne — une valeur extrême fausserait la moyenne, alors que p50 donne le ressenti typique et p95 le pire cas réaliste.

| Option | Latence p50 | Latence p95 | Qualité QCM | Reste local (RGPD) ? |
|---|---|---|---|---|
| Llama 3.1 8B (ne rien changer) | ~72 s | ~95 s | Bonne, bon français | Oui |
| Mistral 7B | ~60 s | ~78 s | Correcte | Oui |
| **Phi-3-mini (3.8B)** | **~30 s** | **~42 s** | Acceptable, à surveiller | **Oui** |
| Fournisseur externe (OpenAI) | rapide | rapide | Très bonne | **Non — écarté** |

## 3. Décision retenue

On remplace Llama 3.1 8B par **Phi-3-mini** comme modèle par défaut, en restant sur Ollama local, et on place le choix derrière un *feature flag* (`LLM_MODEL`) pour pouvoir revenir en arrière sans toucher au code.

## 4. Justification

Phi-3-mini divise la latence par plus de 2 (p50 ~30 s contre ~72 s) tout en gardant une qualité de QCM suffisante pour le MVP. Mistral 7B améliore trop peu la latence pour une qualité proche de Llama. L'option externe (OpenAI) aurait été la plus rapide mais a été écartée d'office : elle viole la contrainte RGPD, qui est l'argument différenciant non négociable d'EduTutor. L'option « ne rien changer » est rejetée car la latence actuelle fait fuir l'utilisateur avant la fin de la génération.

## 5. Conséquences

**Positives**
- Latence divisée par plus de 2 : l'attente devient acceptable.
- On reste 100 % local : contrainte RGPD / souveraineté tenue.
- Coût nul (pas d'appel API payant).
- Le feature flag permet un retour arrière immédiat.

**Négatives / à surveiller**
- Phi-3-mini est plus petit : moins solide sur le français long, risque de formulations maladroites ou d'erreurs factuelles. À relier à la perturbation J4 (erreurs signalées par Mme Lefèvre) → prévoir une vérification qualité des questions.
- Llama 3.1 8B reste installé en fallback : pas de gain de place disque.
- Choix à réévaluer en Release 2, notamment avec l'arrivée du RAG qui ancrera les générations sur le cours fourni.


