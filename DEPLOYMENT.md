# Déploiement GitHub Pages

Ce projet est un site statique sans étape de build.

## Structure

- `index.html` : point d’entrée publié par GitHub Pages.
- `assets/css/styles.css` : styles de la présentation.
- `assets/js/data.js` : contenu des niveaux.
- `assets/js/app.js` : logique interactive.
- `README.md` : règles et principes de qualité du projet.

## Activer GitHub Pages

1. Pousser le projet sur GitHub.
2. Ouvrir le dépôt sur GitHub.
3. Aller dans `Settings > Pages`.
4. Choisir `Deploy from a branch`.
5. Sélectionner la branche `main`.
6. Sélectionner le dossier `/root`.
7. Valider.

GitHub publie ensuite le site à une URL de ce type :

```text
https://<compte-github>.github.io/<nom-du-repo>/
```

## Vérification locale

Le site peut être ouvert directement avec `index.html`.

Pour une vérification plus proche de GitHub Pages, lancer un serveur statique local depuis la racine du projet :

```powershell
python -m http.server 8000
```

Puis ouvrir :

```text
http://localhost:8000/
```
