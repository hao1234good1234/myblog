from celery import shared_task
import time

@shared_task
def send_welcome_email(user_email):
    """
    模拟发送欢迎邮件（耗时操作）
    :param user_email:
    :return:
    """
    print(f"[Celery] 正在发送欢迎邮件给{user_email}...")
    time.sleep(20) # 模拟网络延迟
    print("[Celery] 邮件发送成功")
    return f"welcome email sent to {user_email}"