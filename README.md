# Filesign

**Filesign** est un outil développé par **trhacknon** permettant d'ajouter ou de vérifier une signature (hash ou watermark) dans différents types de fichiers : images (JPEG/PNG), fichiers audio (MP3) et fichiers vidéo (MP4). Il permet de garantir l'authenticité des fichiers en intégrant une signature dans leurs métadonnées ou dans leurs pixels.

## Fonctionnalités

- **Signature EXIF pour images** : Ajoutez une signature dans les métadonnées EXIF d'une image JPEG/PNG.
- **Watermark invisible pour images** : Insérez une signature invisible dans les pixels d'une image JPEG/PNG.
- **Signature dans les fichiers MP3** : Ajoutez une signature dans les métadonnées d'un fichier audio MP3.
- **Signature dans les fichiers MP4** : Ajoutez une signature dans les métadonnées d'un fichier vidéo MP4.
- **Vérification de signatures** : Vérifiez si une image, un fichier audio ou vidéo contient une signature valide (via EXIF ou watermark).

## Installation

1. Clonez ce dépôt GitHub sur votre machine :
    ```bash
    git clone https://github.com/tucommenceapousser/filesign.git
    ```
2. Installez les dépendances Python nécessaires via `pip` :
    ```bash
    pip install -r requirements.txt
    ```

## Utilisation

Exécutez le script principal `main.py` :
```bash
python main.py
```

Options du menu

1. Signer une image (JPEG/PNG) avec EXIF : Ajoutez une signature dans les métadonnées EXIF.


2. Vérifier une image (JPEG/PNG) avec EXIF : Vérifiez si l'image contient une signature dans ses métadonnées EXIF.


3. Signer une image (JPEG/PNG) avec un watermark invisible : Intégrez une signature invisible directement dans les pixels de l'image.


4. Vérifier une image (JPEG/PNG) pour un watermark invisible : Vérifiez si l'image contient une signature invisible.


5. Signer un fichier audio (MP3) : Ajoutez une signature dans les métadonnées d'un fichier MP3.


6. Vérifier un fichier audio (MP3) : Vérifiez si un fichier MP3 contient une signature.


7. Signer un fichier vidéo (MP4) : Ajoutez une signature dans les métadonnées d'un fichier MP4.


8. Vérifier un fichier vidéo (MP4) : Vérifiez si un fichier MP4 contient une signature.



Exemples

Exemple : Ajouter une signature EXIF à une image PNG

Choisissez une option : 1
Entrez le chemin du fichier : /chemin/vers/image.png
Entrez la signature (votre nom, etc.) : trhacknon

Exemple : Vérifier une signature invisible dans une image JPEG

Choisissez une option : 4
Entrez le chemin du fichier : /chemin/vers/image.jpg
Entrez la signature (votre nom, etc.) : trhacknon

Pré-requis

Python 3.x

Modules Python :

Pillow : Pour la manipulation d'images (PNG/JPEG).

mutagen : Pour la manipulation de fichiers MP3/MP4.

numpy : Pour le traitement des pixels d'image.



Installez les pré-requis avec :

pip install Pillow mutagen numpy

Auteur

Développé par trhacknon.

License

Ce projet est sous licence MIT - voir le fichier LICENSE pour plus de détails.
