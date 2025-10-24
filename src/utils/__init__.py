"""
Utils package for Discord Music Bot
"""
from .song import Song
from .queue_manager import QueueManager
from .youtube_handler import YouTubeHandler
from .spotify_handler import SpotifyHandler
from .embeds import (
    create_now_playing_embed,
    create_queue_embed,
    create_search_results_embed,
    create_error_embed,
    create_success_embed
)

__all__ = [
    'Song',
    'QueueManager',
    'YouTubeHandler',
    'SpotifyHandler',
    'create_now_playing_embed',
    'create_queue_embed',
    'create_search_results_embed',
    'create_error_embed',
    'create_success_embed'
]
