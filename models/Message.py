from importlib.resources import contents
from emoji_encodings import encodings

class Message:

    def __init__(self, message_obj: dict) -> None:
        # extract relevant values from raw data
        self.discord_id = message_obj.get('id')
        self.content = message_obj.get('content', None)
        reactions = message_obj.get('reactions', [])

        # creating dict property containing counts for rofl and joy emojis
        self.funny_emoji_counts = self._generate_funny_emoji_counts(reactions)
    
            
        # convenience property for filtering funny messages
        self.has_funny_emojis = len(self.funny_emoji_counts.keys()) > 0


    def _generate_funny_emoji_counts(self, reactions) -> dict:
        funny_emoji_counts = {}
        # assign dict property
        for reaction in reactions:

            # extract relevant values from reaction object
            name = reaction['emoji']['name']
            count = reaction['count']

            # funny_emoji_count object will be empty if reacction has no funny emojis
            # if name not in [encodings['rofl'], encodings['joy']]:
            #     continue

            # add relevant emojis to funny emoji count object
            if name in [encodings['rofl'], encodings['joy']]:
                funny_emoji_counts[name] = count
                
        return funny_emoji_counts