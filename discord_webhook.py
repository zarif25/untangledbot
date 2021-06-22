from dhooks import Webhook as __Webhook

__hook = __Webhook(
    'https://discord.com/api/webhooks/854931544056397844/K4GxmcMf085qBudcAuJh0mStT1gS4dxjoP6BpJJwdabM1y6FXMSE-UuDvDf0x4_suF-z')

def log_error_to_discord(content: str):
    __hook.send(content, username="Error")

def log_success_to_discord(content: str):
    __hook.send(f"{content}\n@here", username="Success")

def log_info_to_discord(content: str):
    return
    __hook.send(f"{content}", username="Info")
