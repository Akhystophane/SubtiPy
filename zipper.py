from zipfile import ZipFile
import os


def remove_macosx_from_zip(zip_path):
    # Chemin temporaire pour la nouvelle archive sans le dossier __MACOSX
    new_zip_path = zip_path[:-4] + '_no_macosx.zip'

    # Ouvrir l'archive existante en mode lecture
    with ZipFile(zip_path, 'r') as zip_ref:
        # Créer une nouvelle archive sans le dossier __MACOSX
        with ZipFile(new_zip_path, 'w') as new_zip_ref:
            for item in zip_ref.infolist():
                if '__MACOSX/' not in item.filename:
                    content = zip_ref.read(item.filename)
                    new_zip_ref.writestr(item, content)

    print(f"Created new ZIP file without __MACOSX at {new_zip_path}")


# Chemin de l'archive ZIP existante
zip_path = '/Users/emmanuellandau/Documents/DONE/HomerSimpson.zip'

remove_macosx_from_zip(zip_path)
