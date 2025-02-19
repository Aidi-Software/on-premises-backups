- [Aidi On-Premises Backup](#aidi-on-premises-backup)
  - [Quickstart](#quickstart)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Execution](#execution)
  - [Usage](#usage)
  - [Examples](#examples)
- [Sauvegardes Aidi Sur-Site](#sauvegardes-aidi-sur-site)
  - [Démarrage rapide](#démarrage-rapide)
  - [Prérequis](#prérequis)
  - [Installation](#installation-1)
  - [Exécution](#exécution)
  - [Utilisation](#utilisation)
  - [Exemples](#exemples)

# Aidi On-Premises Backup

Aidi On-Premise Backup script

Generates a backup of an Aidi instance locally. Is essentially a wrapper for a boto3 connection to an AWS S3 bucket. 

This script is meant to backup an Aidi instance locally. It is not meant to extract or manipulate Aidi's data. The structure and content of the data returned by this script may change over time without notice. 
As a result, the data returned by this script should not be used for business logic, reporting, or any other application beyond backups. Aidi is not responsible for any issues arising from the use of this script outside its intended purpose.

## Quickstart
- Obtain an Aidi backup bucket name, an Aidi backup access key and an Aidi backup secret key from your Aidi customer representative.
- Make sure you have `python3` installed.
- Download the latest release from [release page](https://github.com/Aidi-Software/on-premises-backups/releases)
- From the unzipped directory, run `python3 -m pip install -r requirements.txt`
- From the unzipped directory, run the following command:
```
python3 aidi-on-premises-backup.py -b <backup_bucket_name> -a <backup_access_key> -s <backup_secret_key> -t /path/to/backup -f true -o false
```

## Prerequisites

A valid `python3` installation must be available on the operating system. Verify that a valid Python installation is present by typing  `python3 --version` in a terminal.

You must contact your Aidi Customer representative to obtain the following informations:
- The backup bucket names. You may be given two bucket names: One for the database backups, and one for the filesystem. If that is the case, the command must be executed twice.
- The backup access key
- The backup secret key.

## Installation

1. Go to the [release page](https://github.com/Aidi-Software/on-premises-backups/releases) of this repository and download the lastest release
2. Unzip the folder and open a terminal at the root of the unzipped folder
3. Run the following command: `python3 -m pip install -r requirements.txt`

## Execution

1. Open a terminal at the root of the unzipped folder
2. Run the following command: `python3 aidi-on-premises-backup.py --help` to see all the parameters

## Usage

```
python3 aidi-on-premises-backup.py 
    -b|--aidi-backup-bucket <aidi_backup_bucket_name> 
    -a|--aidi-backup-access-key <aidi_backup_access_key> 
    [-s|--aidi-backup-secret-key <aidi_backup_secret_key>] 
    -t|--target-directory <target_directory> 
    [-f|--force-create-directory <force_create_directory>] 
    [-o|--overwrite-existing-files <overwrite_existing_files>]
```
-  `-b|--aidi-backup-bucket <aidi_backup_bucket_name>` (Required): Name of the bucket to fetch data from. Given by your Aidi customer service representative. The command must be executed once per bucket to backup. Example: `backup-fs-my-environment-name`.
-  `-a|--aidi-backup-access-key <aidi_backup_access_key>` (Required): Access key as given by your Aidi customer service representative. Example: `ABCDEFGHIJ1234567890`
-  `-s|--aidi-backup-secret-key <aidi_backup_secret_key>`: Secret key as given by your Aidi customer service representative. Can also be provided using the the `AIDI_BACKUP_SECRET_KEY` environment variable for improved security, if not provided as a command-line argument. Example: `aBcDeFgHiJkLmNoPqRsTuVwXyZ+1234567890123`
- `-t|--target-directory <target_directory>` (Required): The target directory where the backup should be located. Example: `/tmp/backup-2025-02-08`
- `-f|--force-create-directory <force_create_directory>`: Whether the directory (and all its parents) should automatically be created or not if they do not exist. May exVit if this script is not given permission to create the directory. Defaults to `false`.
- `-o|--overwrite-existing-files <overwrite_existing_files>`: Overwrites the downloaded files if they do not already exist. Defaults to `false`.

## Examples

Downloading all files from the bucket named `backup-fs-my-environment-name` into `C:\backup-2025-25-08` (create the folder automatically), given the access key `ABCDEFGHIJ1234567890` and secret key `aBcDeFgHiJkLmNoPqRsTuVwXyZ+1234567890123`:
```
python3 aidi-on-premises-backup.py -b backup-fs-my-environment-name -a ABCDEFGHIJ1234567890 -s aBcDeFgHiJkLmNoPqRsTuVwXyZ+1234567890123 -t C:\backup-2025-25-08 -f true
```

Downloading only the new files (since last time the backup was executed) from the bucket named `backup-my-environment-name` into the existing folder `/home/admin/aidi-backup` , given the access key `ABCDEFGHIJ1234567890` and secret key `aBcDeFgHiJkLmNoPqRsTuVwXyZ+1234567890123`:
```
python3 aidi-on-premises-backup.py -b backup-my-environment-name -a ABCDEFGHIJ1234567890 -s aBcDeFgHiJkLmNoPqRsTuVwXyZ+1234567890123 -t /home/admin/aidi-backup
```

# Sauvegardes Aidi Sur-Site 

Script de sauvegarde sur site Aidi

Génère une sauvegarde d'une instance Aidi localement. Est essentiellement une surcouche pour une connexion boto3 à un bucket AWS S3. 

Ce script est destiné à sauvegarder votre instance Aidi localement. Il n'est pas destiné à extraire ou manipuler les données d'Aidi. La structure et le contenu des données renvoyées par ce script peuvent changer sans préavis. 
Par conséquent, les données renvoyées par ce script ne doivent pas être utilisées à des fins de logique applicative, de création de rapports ou pour toute autre application autre que les sauvegardes. Aidi n'est pas responsable des problèmes résultant de l'utilisation de ce script en dehors de son objectif prévu.

## Démarrage rapide
- Obtenez un nom de bucket de sauvegarde Aidi, une clé d'accès de sauvegarde Aidi et une clé secrète de sauvegarde Aidi auprès de votre représentant client Aidi
- Assurez-vous d'avoir `python3` installé
- Téléchargez la dernière version depuis [page de publication](https://github.com/Aidi-Software/on-premises-backups/releases)
- Depuis le répertoire décompressé, exécutez `python3 -m pip install -r requirements.txt`
- Depuis le répertoire décompressé, exécutez la commande suivante :
```
python3 aidi-on-premises-backup.py -b <nom_bucket_sauvegarde> -a <cle_acces_sauvegarde> -s <cle_secrete_sauvegarde> -t /emplacement/de/la/sauvegarde -f true -o false
```

## Prérequis

Une installation `python3` valide doit être disponible sur le système d'exploitation. Vérifiez qu'une installation Python valide est présente en saisissant `python3 --version` dans un terminal.

Vous devez contacter votre représentant client Aidi pour obtenir les informations suivantes :
- Les noms des buckets de sauvegarde. Deux noms de buckets peuvent vous être attribués : un pour les sauvegardes de base de données et un pour le système de fichiers. Si tel est le cas, la commande doit être exécutée deux fois.
- La clé d'accès de sauvegarde
- La clé secrète de sauvegarde.

## Installation

1. Accédez à la [page de publication](https://github.com/Aidi-Software/on-premises-backups/releases) de ce répertoire et téléchargez la dernière version
2. Décompressez le dossier et ouvrez un terminal à la racine du dossier décompressé
3. Exécutez la commande suivante : `python3 -m pip install -r requirements.txt`

## Exécution

1. Ouvrez un terminal à la racine du dossier décompressé
2. Exécutez la commande suivante : `python3 aidi-on-premises-backup.py --help` pour voir tous les paramètres

## Utilisation

```
python3 aidi-on-premises-backup.py 
    -b|--aidi-backup-bucket <aidi_backup_bucket_name> 
    -a|--aidi-backup-access-key <aidi_backup_access_key> 
    [-s|--aidi-backup-secret-key <aidi_backup_secret_key>] 
    -t|--target-directory <target_directory> 
    [-f|--force-create-directory <force_create_directory>] 
    [-o|--overwrite-existing-files <overwrite_existing_files>]
```
- `-b|--aidi-backup-bucket <aidi_backup_bucket_name>` (Obligatoire) : nom du bucket à partir duquel récupérer les données. Fourni par votre représentant client Aidi. La commande doit être exécutée une fois par bucket à sauvegarder. Exemple : `backup-fs-my-environment-name`.
- `-a|--aidi-backup-access-key <aidi_backup_access_key>` (Obligatoire) : clé d'accès telle que fournie par votre représentant client Aidi. Exemple : `ABCDEFGHIJ1234567890`
- `-s|--aidi-backup-secret-key <aidi_backup_secret_key>` : clé secrète fournie par votre représentant client Aidi. Peut également être fournie à l'aide de la variable d'environnement `AIDI_BACKUP_SECRET_KEY` pour une sécurité améliorée, si elle n'est pas fournie comme argument de ligne de commande. Exemple : `aBcDeFgHiJkLmNoPqRsTuVwXyZ+1234567890123`
- `-t|--target-directory <target_directory>` (obligatoire) : répertoire cible dans lequel la sauvegarde doit être située. Exemple : `/tmp/backup-2025-02-08`
- `-f|--force-create-directory <force_create_directory>` : indique si le répertoire (et tous ses parents) doivent être créés automatiquement ou non s'ils n'existent pas. Le script peux arréter son exécution s'il n'a pas l'autorisation de créer le répertoire. La valeur par défaut est `false`.
- `-o|--overwrite-existing-files <overwrite_existing_files>` : remplace les fichiers téléchargés s'ils n'existent pas déjà. La valeur par défaut est `false`.

## Exemples

Téléchargement de tous les fichiers du bucket nommé `backup-fs-my-environment-name` dans `C:\backup-2025-25-08` (créer le dossier automatiquement), étant donné la clé d'accès `ABCDEFGHIJ1234567890` et la clé secrète `aBcDeFgHiJkLmNoPqRsTuVwXyZ+1234567890123`. :
```
python3 aidi-on-premises-backup.py -b backup-fs-my-environment-name -a ABCDEFGHIJ1234567890 -s aBcDeFgHiJkLmNoPqRsTuVwXyZ+1234567890123 -t C:\backup-2025-25-08 -f true
```

Téléchargement uniquement des nouveaux fichiers (depuis la dernière fois la sauvegarde a été exécutée) à partir du bucket nommé `backup-my-environment-name` dans le dossier existant `/home/admin/aidi-backup`, étant donné la clé d'accès `ABCDEFGHIJ1234567890` et la clé secrète `aBcDeFgHiJkLmNoPqRsTuVwXyZ+1234567890123`:
```
python3 aidi-on-premises-backup.py -b backup-my-environment-name -a ABCDEFGHIJ1234567890 -s aBcDeFgHiJkLmNoPqRsTuVwXyZ+1234567890123 -t /home/admin/aidi-backup -o false
```
