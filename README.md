# Projet AWS Amplify – React + Vite

Ce projet combine une application front-end React (avec Vite) et un back-end serverless basé sur AWS Amplify. Il permet la gestion d'utilisateurs via des fonctions Lambda exposées par API Gateway.

## Fonctionnalités principales

- **Front-end** : Application React rapide et moderne, développée avec Vite.
- **Back-end** : Fonctions Lambda pour la gestion des utilisateurs (création, récupération, etc.), orchestrées par AWS Amplify.
- **Base de données** : Stockage des utilisateurs via DynamoDB (géré par Amplify Storage).
- **Authentification** : Gérée par Amplify Auth (Cognito).

## Routes API

- **GET /get** : Récupère les informations d'un utilisateur (fonction Lambda `getUser`).
- **POST /post** : Crée un nouvel utilisateur (fonction Lambda `postUser`).

Voir les exemples de payloads et de réponses dans le fichier `README_API.md`.

## Tests

Les tests unitaires des fonctions Lambda sont situés dans `amplify/tests/` :

- `test_get_lambda.py` : Teste la récupération d'utilisateur.
- `test_post_lambda.py` : Teste la création d'utilisateur.
- `test_lambda.py` et `test_.py` : Autres tests.

Pour exécuter les tests :

```bash
cd amplify/tests
pytest
```

## Structure du projet

- `src/` : Code source React.
- `amplify/` : Configuration Amplify, fonctions Lambda, tests, etc.
- `amplify/backend/function/` : Code source des Lambdas.
- `amplify/tests/` : Tests unitaires Python.

## Démarrage rapide

1. Installer les dépendances front-end :
   ```bash
   npm install
   ```
2. Lancer le front-end :
   ```bash
   npm run dev
   ```
3. Pour déployer ou tester le back-end, utiliser les commandes Amplify (`amplify push`, etc.).

Pour plus de détails sur les routes et les tests, consultez le fichier `README_API.md`.
