# API Gestion de rendez vous (Django Rest Framework)

# Description
Cette API permet de gérer la prise de rendez-vous au sein d’une organisation.
Elle offre un système complet de gestion des utilisateurs, des disponibilités, des créneaux bloqués et des notifications, avec des règles métier adaptées à un contexte professionnel (administration, direction, gestionnaires).

Le projet est développé avec Django REST Framework et suit une architecture claire et évolutive.

# Fonctionnalités principales 

*Gestion des utilisateurs 
    Inscription des utilisateurs

    Authentification via JWT

    Rôles : admin, manager, user

    Mise à jour du profil utilisateur

    Suppression des utilisateurs (réservée aux administrateurs)

*Gestion des rendez-vous
    Création de rendez-vous par les utilisateurs

    Limitation à un seul rendez-vous en attente par utilisateur

    Modification et suppression selon le rôle (Seuls les manager et superuser) et le statut(Non accepté )

    Validation ou refus par les gestionnaires / administrateurs

*Horaires de travail (TimeWorks)

    Définition des horaires de travail par un gestionnaire

    Affichage informatif (non bloquant) pour les utilisateurs

    Possibilité de mettre à jour les horaires existants

*Indisponibilités (CalendarBlock)

    Blocage de créneaux horaires par un gestionnaire ou superUser

    Empêche la prise de rendez-vous sur une période indisponible

Notifications

    Notification automatique lors de certaines actions (ex : modification d’un rendez-vous)



