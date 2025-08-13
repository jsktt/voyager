import os
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials

load_dotenv()

def check_credentials():
    """Check if all required Spotify credentials are available"""
    if not all([
        os.getenv('SPOTIFY_CLIENT_ID'),
        os.getenv('SPOTIFY_CLIENT_SECRET'),
        os.getenv('SPOTIFY_REDIRECT_URI')
    ]):
        raise ValueError("Missing Spotify credentials in .env file")

def get_user_spotify_client():
    """
    Get Spotify client with user authentication for accessing user data
    (like top tracks, playlists, etc.)
    """
    check_credentials()
    
    # Clear existing cache to force fresh authentication
    cache_path = ".cache_user"
    if os.path.exists(cache_path):
        os.remove(cache_path)
        print("Cleared existing user cache")

    try:
        auth_manager = SpotifyOAuth(
            client_id=os.getenv('SPOTIFY_CLIENT_ID'),
            client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
            redirect_uri=os.getenv('SPOTIFY_REDIRECT_URI'),
            scope="user-library-read playlist-read-private user-top-read user-read-recently-played",
            open_browser=True,
            cache_path=cache_path,
            show_dialog=True
        )

        # Get token explicitly
        token_info = auth_manager.get_access_token(as_dict=False)
        print(f"User token obtained: {token_info[:20]}...")

        # Create Spotify client with auth manager
        sp = spotipy.Spotify(auth_manager=auth_manager)

        # Verify connection
        user = sp.current_user()
        print(f"Successfully connected to account: {user['display_name']}")
        
        return sp

    except Exception as e:
        print(f"User Authentication Error: {str(e)}")
        raise

def get_public_spotify_client():
    """
    Get Spotify client with client credentials for accessing public data
    SKIP TEST IN DEVELOPMENT MODE
    """
    check_credentials()
    
    try:
        # Client Credentials flow for public data
        client_credentials_manager = SpotifyClientCredentials(
            client_id=os.getenv('SPOTIFY_CLIENT_ID'),
            client_secret=os.getenv('SPOTIFY_CLIENT_SECRET')
        )
        
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        
        # Skip the test that's causing issues
        print("✓ Public client created (test skipped due to Development Mode)")
        return sp
            
    except Exception as e:
        print(f"Public Authentication Error: {str(e)}")
        # Return None so we fall back to user client
        return None

def get_spotify_clients():
    """
    Get both user and public Spotify clients
    Returns: (user_client, public_client)
    """
    print("Setting up Spotify authentication...")
    print("⚠️  Development Mode: Some API restrictions may apply")
    
    user_client = get_user_spotify_client()
    public_client = get_public_spotify_client()
    
    # If public client setup failed, use user client for everything
    if public_client is None:
        print("⚠️  Public client failed - using user client for all requests")
        public_client = user_client
    
    print("✓ Spotify clients ready!")
    return user_client, public_client