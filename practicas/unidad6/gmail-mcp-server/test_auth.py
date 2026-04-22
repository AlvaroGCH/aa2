"""Script de prueba rápida para verificar la autenticación OAuth.

Ejecuta: uv run test_auth.py

La primera vez abrirá el navegador para autorizar acceso a Gmail
y generará token.json. Las siguientes veces ya no pedirá nada.
"""
from gmail_mcp_server import get_gmail_service


if __name__ == "__main__":
    service = get_gmail_service()
    profile = service.users().getProfile(userId="me").execute()
    print("Autenticacion OK")
    print(f"Email: {profile['emailAddress']}")
    print(f"Total mensajes: {profile['messagesTotal']}")
    print(f"Hilos totales: {profile['threadsTotal']}")
