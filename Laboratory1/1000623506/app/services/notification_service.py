from app.channels.email_channel import EmailChannel
from app.channels.sms_channel import SMSChannel

def build_channel_chain(available_channels):
    chain = None
    for ch in reversed(available_channels):
        if ch == 'email':
            chain = EmailChannel(successor=chain)
        elif ch == 'sms':
            chain = SMSChannel(successor=chain)
    return chain
