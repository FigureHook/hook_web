from hook_tasks.on_demand.tasks import send_discord_webhook


def send_notification_hook(webhook_id: int, webhook_token: str, msg: str):
    send_discord_webhook(webhook_id, webhook_token, msg)
    # send_discord_webhook.apply_async(kwargs={
    #     'webhook_id': webhook_id,
    #     'webhook_token': webhook_token,
    #     'msg': msg
    # })
