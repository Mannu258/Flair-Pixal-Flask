def is_playlist(youtube_link):
    if "list=" in youtube_link:
        return True
    else:
        return False

# Example usage
youtube_link = "https://www.youtube.com/watch?v=juZN67BA_5w&list=RDjuZN67BA_5w&start_radio=1"
if is_playlist(youtube_link):
    print("The provided link is a playlist.")
else:
    print("The provided link is a single video.")
