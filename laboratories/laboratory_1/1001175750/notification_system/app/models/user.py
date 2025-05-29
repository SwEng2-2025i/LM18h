#e crea la clase de usuario, y se define el constructor con la estructura
class User:
    def __init__(self, name, preferred_channel, available_channels):

        """
        Initialize a new User instance.

        :param name: str - The name of the user.
        :param preferred_channel: str - The user's preferred notification channel (e.g., 'email', 'sms').
        :param available_channels: list of str - List of channels available for the user to receive notifications.
        """
        self.name = name
        self.preferred_channel = preferred_channel
        self.available_channels = available_channels
