from importlib.resources import contents
from emoji_encodings import encodings

class Message:

    def __init__(self, message_obj: dict) -> None:
        self.content = message_obj.get('content', None)
        reactions = message_obj.get('reactions', [])

        # creating dict property containing counts for rolf and joy emojis
        self.funny_emoji_counts = {}
        for reaction in reactions:
            name = reaction['emoji']['name']
            count = reaction['count']

            # continue loop if irrelevant emoji
            if name not in [encodings['rofl'], encodings['joy']]:
                continue

            # assigns key and count property
            self.funny_emoji_counts[name] = count
            
        # convenience property for filtering funny messages
        self.has_funny_emojis = len(self.funny_emoji_counts.keys()) > 0

  