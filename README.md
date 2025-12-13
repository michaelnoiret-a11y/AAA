# Challenge Triple A - Dashboard de Monitoring
Outil simple de monitoring avec un dashboard web qui affiche en temps réel les statistiques d'une machine virtuelle Linux. 
Cette solution doit être légère, autonome et facilement compréhensible par les équipes techniques.
Projet La Plateforme
Bachelor IT B1

## Description
Dashboard web HTML/CSS qui affiche les statistisques d'une machine virtuelle Linux grâce à un script Python qui collecte ses données.

## Prérequis
- Python 3.18+
- La bibliothèque psutil

## Installation

# Commandes pour installer les dépendances
sudo apt install python3-pip ou sudo apt update, sudo apt upgrade dans le terminal Linux
pip install psutil dans le terminal cmd ou powershell Windows

## Utilisation
Utilisable par n'importe qui soucieux de consulter la consommation de son ordinateur

# Comment lancer un script
Utiliser le terminal cmd ou powershell, taper la commande python ou python3 pour pouvoir executer les scripts python.

# Ouvrir index.html dans le navigateur
Pour afficher le dashboard avec les données collectés, ne pas oublier de lancer le script Python avant

## Fonctionnalités
- Collecte de données grâce au script Python.
- Affichage du dashboard HTML/CSS grâce aux templates et le script Python
- Codes couleurs en fonction de la consommation
- Gauge.js pour visualiser la consommation au lieu de données numériques
- Analyses système avancées pour visualiser les détails des statistiques
- Analyse de fichiers approfondies; les extensions de fichiers, l'espace occupé par type de fichiers, etc...
- Rafraichissement automatique du HTML toutes les 30s
## Captures d'écran


## Difficultés rencontrées
- Remplacer les variables génériques par les données collectées
- Lier le script Python au template html
- Trouver les bonnes commandes pour répondre aux demandes de collecte d'informations
- Push projet depuis la machine virtuelle
- Installer psutil
- Travailler en équipe

## Améliorations possibles
- graphiques représentant le pourçentage d'utilisation ainsi que sa durée
- Ajout affichage historique des applications
- Affichage et gestion applications aux démarrages

## Auteur
Alexis Noiret.
Michaël Noiret.
Bachelor IT première année.
La Plateforme.