import hashlib
import os
from PIL import Image, PngImagePlugin
from PIL.ExifTags import TAGS
import numpy as np
import mutagen
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4

# Fonction pour générer une signature SHA-256 à partir d'un fichier
def generate_signature(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

# Fonction pour convertir une chaîne de texte en binaire
def text_to_bin(text):
    return ''.join(format(ord(c), '08b') for c in text)

# Fonction pour convertir un binaire en texte
def bin_to_text(binary):
    chars = [chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8)]
    return ''.join(chars)

# Fonction pour ajouter une signature dans les métadonnées EXIF d'une image JPEG/PNG
def sign_image_with_exif(file_path, signature):
    try:
        img = Image.open(file_path)
        if file_path.lower().endswith('.png'):
            # Pour PNG, on utilise les métadonnées textuelles
            metadata = PngImagePlugin.PngInfo()
            metadata.add_text("Signature", signature)
            img.save(file_path, pnginfo=metadata)
            print(f"Signature EXIF ajoutée à l'image PNG {file_path}.")
        else:
            # Pour JPEG, on utilise les métadonnées EXIF
            exif_dict = img.info.get('exif', b'')
            img.save(file_path, exif=exif_dict)
            print(f"Signature EXIF ajoutée à l'image JPEG {file_path}.")
    except Exception as e:
        print(f"Erreur lors de la signature EXIF : {e}")

# Fonction pour vérifier la signature dans les métadonnées EXIF d'une image
def verify_image_with_exif(file_path, signature):
    try:
        img = Image.open(file_path)
        if file_path.lower().endswith('.png'):
            # Pour PNG, vérifier dans les métadonnées textuelles
            metadata = img.info
            if "Signature" in metadata and metadata["Signature"] == signature:
                print(f"Signature trouvée dans l'image PNG {file_path} (EXIF).")
                return True
            else:
                print(f"Aucune signature trouvée dans l'image PNG {file_path}.")
                return False
        else:
            # Pour JPEG, vérifier dans les métadonnées EXIF
            exif_data = img._getexif()
            if exif_data:
                for tag, value in exif_data.items():
                    tag_name = TAGS.get(tag, tag)
                    if tag_name == 'UserComment' and value == signature:
                        print(f"Signature trouvée dans l'image JPEG {file_path} (EXIF).")
                        return True
            print(f"Aucune signature trouvée dans l'image JPEG {file_path}.")
            return False
    except Exception as e:
        print(f"Erreur lors de la vérification EXIF : {e}")
        return False

# Fonction pour ajouter un watermark invisible dans une image PNG ou JPEG
def sign_image_with_watermark(file_path, signature):
    try:
        img = Image.open(file_path)
        img_data = np.array(img)

        # Convertir la signature en binaire
        sig_bin = text_to_bin(signature)

        # Vérifier que l'image a suffisamment de pixels pour stocker la signature
        if len(sig_bin) > img_data.size * 3:
            raise ValueError("L'image est trop petite pour contenir la signature.")

        # Appliquer le watermark sur les pixels (modifier les bits de couleur)
        idx = 0
        for x in range(img_data.shape[0]):
            for y in range(img_data.shape[1]):
                if idx < len(sig_bin):
                    r, g, b = img_data[x, y][:3]  # Obtenir les valeurs RGB

                    # Modifier les bits LSB (Least Significant Bit) des trois canaux
                    r = (r & 0xFE) | int(sig_bin[idx])
                    if idx + 1 < len(sig_bin):
                        g = (g & 0xFE) | int(sig_bin[idx + 1])
                    if idx + 2 < len(sig_bin):
                        b = (b & 0xFE) | int(sig_bin[idx + 2])

                    # Réinsérer les nouvelles valeurs RGB
                    img_data[x, y][:3] = [r, g, b]
                    idx += 3

        # Sauvegarder l'image avec watermark invisible
        img_with_watermark = Image.fromarray(img_data)
        img_with_watermark.save(file_path)
        print(f"Image {file_path} signée avec succès (watermark invisible ajouté).")
    except Exception as e:
        print(f"Erreur lors de la signature de l'image : {e}")

# Fonction pour vérifier le watermark dans une image PNG ou JPEG
def verify_image_with_watermark(file_path, signature):
    try:
        img = Image.open(file_path)
        img_data = np.array(img)

        # Convertir la signature en binaire
        sig_bin = text_to_bin(signature)
        extracted_sig = []

        # Extraire le watermark des pixels modifiés
        idx = 0
        for x in range(img_data.shape[0]):
            for y in range(img_data.shape[1]):
                if idx < len(sig_bin):
                    r, g, b = img_data[x, y][:3]  # Obtenir les valeurs RGB

                    # Lire les bits LSB des trois canaux
                    extracted_sig.append(str(r & 1))
                    if idx + 1 < len(sig_bin):
                        extracted_sig.append(str(g & 1))
                    if idx + 2 < len(sig_bin):
                        extracted_sig.append(str(b & 1))

                    idx += 3

        # Convertir le watermark extrait en chaîne
        extracted_signature = bin_to_text(''.join(extracted_sig[:len(sig_bin)]))
        if extracted_signature == signature:
            print(f"Signature trouvée dans l'image {file_path} (watermark).")
            return True
        else:
            print(f"Aucune signature trouvée dans l'image {file_path}.")
            return False
    except Exception as e:
        print(f"Erreur lors de la vérification du watermark de l'image : {e}")
        return False

# Fonction pour ajouter une signature dans les métadonnées d'un fichier MP3
def sign_audio_mp3(file_path, signature):
    try:
        audio = MP3(file_path, ID3=mutagen.id3.ID3)
        audio["TXXX:Signature"] = mutagen.id3.TXXX(encoding=3, desc="Signature", text=[signature])
        audio.save()
        print(f"Signature ajoutée au fichier MP3 {file_path}.")
    except Exception as e:
        print(f"Erreur lors de la signature du fichier MP3 : {e}")

# Fonction pour vérifier la signature dans les métadonnées d'un fichier MP3
def verify_audio_mp3(file_path, signature):
    try:
        audio = MP3(file_path, ID3=mutagen.id3.ID3)
        if "TXXX:Signature" in audio and audio["TXXX:Signature"].text[0] == signature:
            print(f"Signature trouvée dans le fichier MP3 {file_path}.")
            return True
        else:
            print(f"Aucune signature trouvée dans le fichier MP3 {file_path}.")
            return False
    except Exception as e:
        print(f"Erreur lors de la vérification du fichier MP3 : {e}")
        return False

# Fonction pour ajouter une signature dans les métadonnées d'un fichier MP4
def sign_video_mp4(file_path, signature):
    try:
        video = MP4(file_path)
        video["©cmt"] = [signature]  # Utilisation du champ commentaire pour ajouter la signature
        video.save()
        print(f"Signature ajoutée au fichier MP4 {file_path}.")
    except Exception as e:
        print(f"Erreur lors de la signature du fichier MP4 : {e}")

# Fonction pour vérifier la signature dans les métadonnées d'un fichier MP4
def verify_video_mp4(file_path, signature):
    try:
        video = MP4(file_path)
        if "©cmt" in video and video["©cmt"][0] == signature:
            print(f"Signature trouvée dans le fichier MP4 {file_path}.")
            return True
        else:
            print(f"Aucune signature trouvée dans le fichier MP4 {file_path}.")
            return False
    except Exception as e:
        print(f"Erreur lors de la vérification du fichier MP4 : {e}")
        return False

# Fonction principale pour interagir avec l'utilisateur
def main():
    print("=== Outil de signature de fichiers par 'trhacknon' ===")
    print("1. Signer une image (JPEG/PNG) avec EXIF")
    print("2. Vérifier une image (JPEG/PNG) avec EXIF")
    print("3. Signer une image (JPEG/PNG) avec un watermark invisible")
    print("4. Vérifier une image (JPEG/PNG) pour un watermark invisible")
    print("5. Signer un fichier audio (MP3)")
    print("6. Vérifier un fichier audio (MP3)")
    print("7. Signer un fichier vidéo (MP4)")
    print("8. Vérifier un fichier vidéo (MP4)")
    print("9. Quitter")

    while True:
        choice = input("Choisissez une option : ")
        if choice == '9':
            print("Quitter...")
            break

        file_path = input("Entrez le chemin du fichier : ")
        signature = input("Entrez la signature (votre nom, etc.) : ")

        if choice == '1':
            sign_image_with_exif(file_path, signature)
        elif choice == '2':
            verify_image_with_exif(file_path, signature)
        elif choice == '3':
            sign_image_with_watermark(file_path, signature)
        elif choice == '4':
            verify_image_with_watermark(file_path, signature)
        elif choice == '5':
            sign_audio_mp3(file_path, signature)
        elif choice == '6':
            verify_audio_mp3(file_path, signature)
        elif choice == '7':
            sign_video_mp4(file_path, signature)
        elif choice == '8':
            verify_video_mp4(file_path, signature)
        else:
            print("Choix non valide, réessayez.")

if __name__ == "__main__":
    main()
