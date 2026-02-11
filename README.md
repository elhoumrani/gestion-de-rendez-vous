# API Gestion de rendez vous (Django Rest Framework)

# Description
Cette API permet de gérer la prise de rendez-vous au sein d’une organisation.
Elle offre un système complet de gestion des utilisateurs, des disponibilités, des créneaux bloqués et des notifications, avec des règles métier adaptées à un contexte professionnel (administration, direction, gestionnaires).

Le projet est développé avec Django REST Framework et suit une architecture claire et évolutive.

## Technologies
- Python 3.12
- Django & Django REST Framework
- MySQL comme SGBD
- Postman pour tests API


# Fonctionnalités principales 

**Gestion des utilisateurs**
    Inscription des utilisateurs

    Authentification via JWT

    Rôles : admin, manager, user

    Mise à jour du profil utilisateur

    Suppression des utilisateurs (réservée aux administrateurs)

**Gestion des rendez-vous**
    Création de rendez-vous par les utilisateurs

    Limitation à un seul rendez-vous en attente par utilisateur

    Modification et suppression selon le rôle (Seuls les manager et superuser) et le statut(Non accepté )

    Validation ou refus par les gestionnaires / administrateurs

**Horaires de travail (TimeWorks)**

    Définition des horaires de travail par un gestionnaire

    Affichage informatif (non bloquant) pour les utilisateurs

    Possibilité de mettre à jour les horaires existants

## Règles métier
- Un utilisateur ne peut avoir qu’un seul rendez-vous en attente.
- Deux rendez-vous ne peuvent pas être pris sur le même créneau.
- Un rendez-vous ne peut pas être pris si la date est bloquée par la direction.
- Un rendez-vous accepté ne peut plus être modifié.
- Seuls les managers ou superusers peuvent modifier le statut d’un rendez-vous.

## Permissions
    **User simple** : créer et consulter ses propres rendez-vous.
    **Manager / Admin** : modifier le statut, commenter les décisions, notifications automatiques.

## Endpoints principaux
- `POST api/appointments/` : créer un rendez-vous
- `PATCH api/appointments/<id>/changer-status/` : modifier le statut d’un rendez-vous
- `GET api/appointments/` : lister ses rendez-vous (admin peut voir tous)

## Historique et notifications
- Toute modification de statut est enregistrée dans `AppointmentDecision`.
- Chaque changement inclut le **responsable, le statut précédent, le nouveau statut et un commentaire facultatif**.
- Les notifications sont envoyées automatiquement aux utilisateurs concernés.

## Tests
- Tests unitaires pour le service métier et les serializers.
- Tests end-to-end pour les permissions et l’API.
- Pour lancer les tests :  
```bash
python manage.py test

