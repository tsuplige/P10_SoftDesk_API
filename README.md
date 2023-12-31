# API SoftDesk

![Version Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Version Django](https://img.shields.io/badge/Django-3.x-green.svg)

Il s'agit de l'API de SoftDesk Support, une application logicielle de collaboration pour le suivi des problèmes techniques. Elle est conçue pour une utilisation Business-to-Business (B2B) et offre des fonctionnalités pour la gestion de projets, de problèmes, de contributeurs et de commentaires.

## Documentation

  - Retrouvé la documentation détaillée sur postman du projet via ce lien : [Documentation](https://documenter.getpostman.com/view/27659986/2s9YRGx9ND)

## Fonctionnalités

- Création et gestion de projets avec des informations détaillées.
- Ajout de contributeurs aux projets.
- Création et gestion de problèmes au sein des projets.
- Commentaire sur les problèmes pour faciliter la collaboration.
- Authentification sécurisée à l'aide de JSON Web Tokens (JWT).
- Conformité aux normes de sécurité et de confidentialité, notamment OWASP et le RGPD.
- Efficacité et optimisation énergétique (Green Code) pour les opérations côté serveur.

## Installation

1. Clonez le dépôt sur votre machine locale :
 ```bash
   git clone https://github.com/tsuplige/P10_SoftDesk_API.git
   
   cd SoftDesk-API
   ```
2. Créez un environnement virtuel et activez-le :

 ```bash
   python -m venv venv
   ```
Sur Windows : venv\Scripts\activate
Sur macOS et Linux : source venv/bin/activate

3. Installez les dépendances du projet :

 ```bash
   pip install -r requirements.txt
   ```

4. Appliquez les migrations de la base de données :

 ```bash
   python manage.py migrate
   ```
5. Lancez le serveur de développement :

 ```bash
   python manage.py runserver
   ```
L'API doit maintenant être accessible à l'adresse `http://localhost:8000`.

## Utilisation

- La documentation de l'API et les points de terminaison sont disponibles à l'adresse `http://localhost:8000/api/`.
- Utilisez un outil tel que [Postman](https://www.postman.com/) ou [curl](https://curl.se/) pour interagir avec l'API.

## Authentification

- Obtenez un jeton d'accès en effectuant une requête POST à l'adresse `http://localhost:8000/api/token/`. Vous devrez fournir votre nom d'utilisateur et votre mot de passe dans le corps de la requête.