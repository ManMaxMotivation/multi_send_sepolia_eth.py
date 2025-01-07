from web3 import Web3
from dotenv import load_dotenv
import os
import time

# Загружаем переменные окружения из .env файла
load_dotenv()

# Получаем приватный ключ и адрес из переменных окружения
private_key = os.getenv("PRIVATE_KEY")
sender_address = os.getenv("SENDER_ADDRESS")

# Подключение к RPC-серверу
rpc_url = "https://1rpc.io/sepolia"  # Замените на ваш RPC URL
web3 = Web3(Web3.HTTPProvider(rpc_url))

# Убедитесь, что соединение установлено
if not web3.is_connected():
    raise Exception("Не удалось подключиться к сети!")


# Функция для отправки ETH
def send_eth(recipient_address, amount_in_eth):
    # Получаем nonce для отправителя
    nonce = web3.eth.get_transaction_count(sender_address)

    # Получаем текущую цену газа
    gas_price = web3.eth.gas_price  # текущая цена газа

    # Увеличиваем цену газа в 1.3 раза для повышения вероятности успешной транзакции
    gas_price = int(gas_price * 1.3)

    # Подготовка транзакции
    tx = {
        'to': recipient_address,
        'value': web3.to_wei(amount_in_eth, 'ether'),  # Используем to_wei вместо toWei
        'gas': 2000000,
        'gasPrice': web3.to_wei('20', 'gwei'),
        'nonce': nonce,
        'chainId': 11155111  # Для сети Sepolia
    }

    # Подпись транзакции
    signed_tx = web3.eth.account.sign_transaction(tx, private_key)

    # Отправка транзакции
    try:
        tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
        print(f"Транзакция отправлена с хэшем: {web3.to_hex(tx_hash)}")

        # Задержка в 1 секунду между транзакциями
        time.sleep(1)

        # Возвращаем хэш транзакции для последующей проверки
        return tx_hash

    except Exception as e:
        print(f"Ошибка отправки транзакции: {e}")
        return None


# Функция для проверки статуса транзакции
def check_transaction_status(tx_hash):
    try:
        # Получаем квитанцию о транзакции
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)  # Ожидаем 120 секунд

        # Проверяем статус транзакции
        if receipt['status'] == 1:
            print(f"Транзакция с хэшем {web3.to_hex(tx_hash)} была успешно подтверждена.")
        else:
            print(f"Транзакция с хэшем {web3.to_hex(tx_hash)} не прошла.")
    except Exception as e:
        print(f"Ошибка при проверке транзакции: {e}")


# Список получателей
recipients = [
    {"address": "WALLET", "amount": 0.001},
    {"address": "WALLET", "amount": 0.001},
    {"address": "WALLET", "amount": 0.001},
    {"address": "WALLET", "amount": 0.001},
    {"address": "WALLET", "amount": 0.001},
    {"address": "WALLET", "amount": 0.001},
    {"address": "WALLET", "amount": 0.001},
    {"address": "WALLET", "amount": 0.001},
    {"address": "WALLET", "amount": 0.001},
    {"address": "WALLET", "amount": 0.001}
]

# Список для хранения хэшей транзакций
transaction_hashes = []

# Отправка транзакций всем получателям с проверкой статуса
for recipient in recipients:
    # Отправляем транзакцию
    tx_hash = send_eth(recipient["address"], recipient["amount"])
    if tx_hash:
        print(f"Транзакция отправлена с хэшем: {web3.to_hex(tx_hash)}")

        # Проверяем статус отправленной транзакции
        check_transaction_status(tx_hash)

        # Добавляем хэш транзакции в список
        transaction_hashes.append(tx_hash)
    else:
        print(f"Не удалось отправить транзакцию на {recipient['address']}")

# Записываем хэши в файл для дальнейшей проверки
with open('tx_hashes.txt', 'w') as file:
    for tx_hash in transaction_hashes:
        file.write(f"{web3.to_hex(tx_hash)}\n")