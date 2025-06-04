Ce projet est le backend d'une application web de recommandations de films, construit avec Flask et utilisant le dataset MovieLens 100K. Il fournit une API REST qui recommande des films par genre (Action, Comédie, etc.) via un algorithme de filtrage collaboratif basé sur la similarité cosinus.

Fonctionnalités

API REST avec une route /recommend (POST) pour obtenir des recommandations par genre. Précalcul des recommandations pour des réponses rapides (< 1 seconde). Support de 19 genres de films (Action, Adventure, Drama, etc.). Intégration avec le dataset MovieLens 100K. Gestion des erreurs et CORS pour les requêtes frontend.

Prérequis

Python (3.8 ou supérieur) : Télécharger. Conda (optionnel, pour gérer les environnements) : Télécharger. Un frontend React configuré (voir recom-stream-front).

Installation

Cloner le repository : git clone https://github.com/votre-utilisateur/recom-stream-backend.git cd recom-stream-backend

Créer un environnement virtuel (optionnel avec Conda) : conda create -n ds_env python=3.11 conda activate ds_env

Installer les dépendances : pip install -r requirements.txt

Exécution locale : python api/app.py
