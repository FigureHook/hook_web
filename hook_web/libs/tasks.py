def send_notification_hook(webhook_id: str, webhook_token: str, msg: str):
    # TODO: prevent call celery function directly
    raise NotImplementedError
    # send_new_hook_notification.apply_async(kwargs={
    #     'webhook_id': webhook_id,
    #     'webhook_token': webhook_token,
    #     'msg': msg
    # })