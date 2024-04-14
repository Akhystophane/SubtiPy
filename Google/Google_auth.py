from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os.path

# Scopes définissent les niveaux d'accès. Si vous avez juste besoin de sauvegarder, "https://www.googleapis.com/auth/drive.file" devrait suffire.
SCOPES = ['https://www.googleapis.com/auth/drive']

creds = None
# Le fichier token.json stocke les tokens d'accès et de rafraîchissement de l'utilisateur.
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
# Si aucun token valide n'existe, on laisse l'utilisateur se connecter.
if not creds or not creds.valid:
    # if creds and creds.expired and creds.refresh_token:
    #     creds.refresh(Request())
    # else:
    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json', SCOPES)
    # Modifier ici pour utiliser un port fixe au lieu de choisir dynamiquement
    creds = flow.run_local_server(port=8080)  # Utilisez le port 8080 au lieu de choisir dynamiquement
    # Sauvegarde du token pour les prochaines exécutions
    with open('token.json', 'w') as token:
        token.write(creds.to_json())
