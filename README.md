# Génération de BCU

Les scripts `list.py` et `export.py`  ont été écrits pour Python 3.8.

Les librairies dont ils dépendent peuvent être installées avec la commande :
```
pip install -r requirements.txt
```

## Prérequis

Tableau Server avec le classeur BCU et un utilisateur pour lequel vous avez généré un jeton d’accès pour l’API REST.

## list.py

L’utilisation de la commande est la suivante :
```
usage: list.py [-h] --server SERVER [--site SITE] --token-name TOKEN_NAME [--token TOKEN]
               [--logging-level {debug,info,error}]
               {workbook,datasource,project,view,job,webhooks}

List out the names and LUIDs for different resource types.

positional arguments:
  {workbook,datasource,project,view,job,webhooks}

optional arguments:
  -h, --help            show this help message and exit
  --server SERVER, -s SERVER
                        server address
  --site SITE, -S SITE  site to log into, do not specify for default site
  --token-name TOKEN_NAME, -n TOKEN_NAME
                        username to signin under
  --token TOKEN, -t TOKEN
                        personal access token for logging in
  --logging-level {debug,info,error}, -l {debug,info,error}
                        desired logging level (set to error by default)
```

Pour lister les vues disponibles, la commande à taper ressemblera à ceci :
```
python list.py -s TABLEAU_SERVER_URL -n NOM_DU_JETON -t SECRET_DU_JETON view
```

Pour chaque vue disponible sur Tableau Server, vous obtiendrez son ID.

## export.py

L’utilisation de la commande est la suivante :
```
usage: export.py [-h] --server SERVER [--site SITE] --token-name TOKEN_NAME [--token TOKEN]
                 [--logging-level {debug,info,error}] [--file FILE]
                 first_resource_id second_resource_id

Export a view as an image, PDF, or CSV

positional arguments:
  first_resource_id     LUID for the first view
  second_resource_id    LUID for the second view

optional arguments:
  -h, --help            show this help message and exit
  --server SERVER, -s SERVER
                        server address
  --site SITE, -S SITE
  --token-name TOKEN_NAME, -n TOKEN_NAME
                        username to signin under
  --token TOKEN, -t TOKEN
                        personal access token for logging in
  --logging-level {debug,info,error}, -l {debug,info,error}
                        desired logging level (set to error by default)
  --file FILE, -f FILE  filename to store the exported data
```

Pour exporter les bordereaux de commission unique au format spécifié par SIMA, il faut avoir récupéré les ID des 2 vues créées spécialement pour l’export des informations du courtier et du détail des affaires.

La commande à taper ressemblera à ceci :
```
python export.py -s TABLEAU_SERVER_URL -n NOM_DU_JETON -t SECRET_DU_JETON ID_FEUILLE_COURTIER ID_FEUILLE_AFFAIRES
```

Le fichier exporté portera le nom `out.csv` à moins de préciser l’option -f.

## Compilation pour Windows

Afin d’éliminer le besoin d’installer Python et les librairies tierces sur l’ordinateur de destination, le script `build.bat` vous permettra de générer une version exécutable pour Windows.

Après l’avoir exécuté, vous trouverez le programme dans le dossier `dist/export` qu’il suffira de transférer sur l’ordinateur de destination.

Il contient les fichier `list.exe` et `export.exe` qui fonctionnent de la même manière que les version Python.
