from web3 import Web3
from dotenv import load_dotenv
import os
import time
from decimal import Decimal

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

    # Увеличиваем цену газа в 1.05 раза для повышения вероятности успешной транзакции
    gas_price = int(gas_price * 1.05)

    # Подготовка транзакции
    tx = {
        'to': recipient_address,
        'value': web3.to_wei(amount_in_eth, 'ether'),
        'gas': int(
            web3.eth.estimate_gas({'to': recipient_address, 'value': web3.to_wei(amount_in_eth, 'ether')}) * 1.05),
        # Преобразуем в целое число
        'gasPrice': gas_price,
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
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)

        # Проверяем статус транзакции
        if receipt['status'] == 1:
            print(f"Транзакция с хэшем {web3.to_hex(tx_hash)} была успешно подтверждена.")
        else:
            print(f"Транзакция с хэшем {web3.to_hex(tx_hash)} не прошла.")
    except Exception as e:
        print(f"Ошибка при проверке транзакции: {e}")

# Функция для проверки валидности Ethereum адреса
def is_valid_ethereum_address(address):
    return Web3.is_address(address)

# Функция для чтения списка адресов из файла
def load_addresses(file_path):
    addresses = []
    with open(file_path, 'r') as file:
        for line in file:
            address = line.strip()
            if address:
                if is_valid_ethereum_address(address):
                    addresses.append(Web3.to_checksum_address(address))  # Преобразуем в checksum-формат
                else:
                    print(f"Некорректный адрес: {address}")
            else:
                print(f"Пустая строка в файле: {line}")
    return addresses

# Путь к файлу с адресами получателей
recipients_file = 'recipients.txt'

# Количество ETH для отправки на один кошелек
amount_in_eth = 0.00001  # Укажите нужное значение

# Загрузка списка адресов из файла
addresses = load_addresses(recipients_file)

# Получаем текущий баланс отправителя
current_balance = web3.from_wei(web3.eth.get_balance(sender_address), 'ether')

# Выводим информацию перед запуском
formatted_amount_in_eth = "{:,.6f}".format(amount_in_eth)
formatted_current_balance = "{:,.6f}".format(current_balance)

# Рассчитываем общую сумму, которую нужно отправить
total_amount = amount_in_eth * len(addresses)
formatted_total_amount = "{:,.6f}".format(total_amount)

# Проверка баланса и газа
total_gas_fee = 0
for address in addresses:
    tx = {
        'to': address,
        'value': web3.to_wei(amount_in_eth, 'ether'),
        'gas': web3.eth.estimate_gas({'to': address, 'value': web3.to_wei(amount_in_eth, 'ether')}) * 1.05,
        'gasPrice': web3.eth.gas_price,
        'nonce': web3.eth.get_transaction_count(sender_address),
        'chainId': 11155111  # Для сети Sepolia
    }
    total_gas_fee += web3.from_wei(tx['gas'] * tx['gasPrice'], 'ether')

# Форматируем для вывода
formatted_gas_fee = "{:,.6f}".format(total_gas_fee)

# Ожидаемая комиссия
total_gas_fee = Decimal(total_gas_fee)
expected_balance = Decimal(current_balance) - Decimal(total_amount) - total_gas_fee
formatted_expected_balance = "{:,.6f}".format(expected_balance)

# Выводим информацию перед запуском
print(f"Информация перед запуском:")
print(f"Отправитель: {sender_address}")
print(f"Сумма на отправку: {formatted_total_amount} ETH (по {formatted_amount_in_eth} ETH на адрес)")
print(f"Баланс отправителя: {formatted_current_balance} ETH")
print(f"Количество получателей: {len(addresses)}")
print(f"Ожидаемый остаток после отправки: {formatted_expected_balance} ETH")
print(f"Ожидаемая комиссия за транзакции: {formatted_gas_fee} ETH")

# Подтверждаем перед запуском
confirmation = input("Если информация верна, введите 'OK' для продолжения: ")

if confirmation.lower() == "ok":
    print("Запуск транзакций...")
    # Список для хранения хэшей транзакций
    transaction_hashes = []

    # Отправка транзакций всем получателям с проверкой статуса
    for address in addresses:
        # Отправляем транзакцию
        tx_hash = send_eth(address, amount_in_eth)
        if tx_hash:
            print(f"Транзакция отправлена с хэшем: {web3.to_hex(tx_hash)}")

            # Проверяем статус отправленной транзакции
            check_transaction_status(tx_hash)

            # Добавляем хэш транзакции в список
            transaction_hashes.append(tx_hash)
        else:
            print(f"Не удалось отправить транзакцию на {address}")

    # Записываем хэши в файл для дальнейшей проверки
    with open('tx_hashes.txt', 'w') as file:
        for tx_hash in transaction_hashes:
            file.write(f"{web3.to_hex(tx_hash)}\n")

    # Получаем остаточный баланс отправителя после всех транзакций
    final_balance = web3.from_wei(web3.eth.get_balance(sender_address), 'ether')
    formatted_final_balance = "{:,.6f}".format(final_balance)

    # Итоговый отчет
    total_transactions = len(transaction_hashes)
    total_eth_sent = total_transactions * amount_in_eth
    total_addresses = len(addresses)

    print(f"\nИтоговый отчет:")
    print(f"Количество отправленных транзакций: {total_transactions}")
    print(f"Общее количество отправленного ETH: {total_eth_sent:.6f}")
    print(f"Количество адресов в списке: {total_addresses}")
    print(f"Остаток на балансе после завершения: {formatted_final_balance} ETH")
else:
    print("Запуск отменен.")