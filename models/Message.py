from emoji_encodings import encodings

class Message:
    def __init__(self, message_obj: dict) -> None:
        self.content = message_obj.get('content', None)
        reactions = message_obj.get('reactions', False)

        self.reactions = list(self._get_reactions(reactions)) if reactions else None

    def _get_reactions(self, reactions):
        for reaction in reactions:
            name = reaction['emoji']['name']
            count = reaction['count']

            if name not in [encodings['rofl'], encodings['joy']]:
                continue

            yield (name, count)
