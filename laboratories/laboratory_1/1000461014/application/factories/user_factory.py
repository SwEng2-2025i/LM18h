from domain.entities.user import User

class UserFactory:
    """
    Factory for creating User instances with validation and normalization.
    """

    def create(self, name: str, preferred_channel: str, available_channels: list[str]) -> User:
        #Normalize channel names for consistency
        preferred_channel_lower = preferred_channel.lower()
        lower_channels_set = {ch.lower() for ch in available_channels}

        #Ensure preferred channel is among the available ones
        if preferred_channel_lower not in lower_channels_set:
            raise ValueError("Preferred channel must be in the list of available channels.")
        
        #Reorder available channels to prioritize the preferred one
        preference_sorted_channels = [preferred_channel_lower] + [
            ch.lower() for ch in available_channels if ch.lower() != preferred_channel_lower
        ]
        
        return User(name = name, preferred_channel = preferred_channel, available_channels = preference_sorted_channels)