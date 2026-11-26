# Gestion des rendez-vous d’un cabinet médical

Projet Django 5.2 LTS pour l’atelier de modélisation et de migrations. `AccountApp` contient `User`, `Doctor`, `Patient` et `Specialty`. `AppointmentApp` contient `Appointment`. Ces modèles sont accessibles depuis l’administration Django.

## Correspondance avec le cours

Le chapitre 1 (p. 20–22 et 29–32) présente l’installation avec `venv` et `pip`, le rôle de `manage.py` et la séparation entre le projet et les applications. Chaque application déclare sa classe `AppConfig` dans `apps.py`. Le projet les enregistre dans `INSTALLED_APPS`.

Le chapitre 2 (diapositives 7–15, 21, 23–27 et 34–36) se retrouve dans les champs et leurs options, les clés étrangères de `Appointment` avec `PROTECT`, la relation `ManyToManyField` entre médecin et spécialité, les validateurs de champs et la méthode `Appointment.clean()`. La classe `Meta` définit l’ordre des rendez-vous et l’unicité du créneau par médecin. Les migrations versionnées créent le schéma SQLite.

La diapositive 38 mentionne le modèle `User` intégré. Le cahier des charges détaillé de l’étude de cas demande `AccountApp.User`, qui hérite de `AbstractUser`. Le projet suit cette consigne pour l’héritage de `Doctor` et `Patient`.

## Démarrage sous Windows

Avec Python 3.12 installé, exécuter ces commandes depuis le dossier du projet.

```powershell
py -3.12 -m venv env
.\env\Scripts\python -m pip install -r requirements.txt
.\env\Scripts\python -m django --version
.\env\Scripts\python manage.py migrate
.\env\Scripts\python manage.py showmigrations AccountApp AppointmentApp
.\env\Scripts\python manage.py createsuperuser
.\env\Scripts\python manage.py runserver
```

Ouvrir l’administration à [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/). Pour ajouter un rendez-vous, enregistrer d’abord une spécialité, un médecin et un patient.

## Base SQLite

Les migrations créent `GestionCabinetMedical.sqlite3` par défaut. Pour utiliser le nom de la classe demandé dans le sujet, définir `$env:CABINET_DB_NAME = "NomDeLaClasse.sqlite3"` avant `migrate` et `runserver`.

Les tables `AccountApp_doctor` et `AccountApp_patient` référencent `AccountApp_user` par leur clé primaire `user_ptr_id`. La table `AccountApp_doctor_specialties` relie les médecins aux spécialités. La base impose l’unicité du créneau pour un même médecin.
