from django.core.mail import send_mail
from django.conf import settings


def process_payment(total_price, payment_data):
    """
    Обрабатывает платеж.
    Args:
        total_price (Decimal): общая сумма для оплаты.
        payment_data (dict): данные для процесса платежа
        (например, данные карты).

    Returns:
        bool: True если платеж прошел успешно, иначе False.
    """
    # Логика обработки платежа (замените на интеграцию с платежной системой)
    # Пример:
    if payment_data["card_number"] == "4242424242424242":
        return True
    else:
        return False


def send_files_to_email(cart, email):
    """
    Отправляет файлы корзины на указанный email.

    Args:
        cart (Cart): объект корзины.
        email (str): электронная почта получателя.
    """
    subject = 'Ваши файлы'
    message = 'Спасибо за покупку. Найдите свои файлы во вложении.'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    attachments = []
    for item in cart.items.all():
        file_path = item.product.file.path
        with open(file_path, 'rb') as file:
            attachments.append((item.product.file.name,
                                file.read(),
                                'application/octet-stream'))
    send_mail(
        subject,
        message,
        from_email,
        recipient_list,
        fail_silently=False,
        html_message=None,
        attachments=attachments
    )
