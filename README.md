# Multi-send Ethereum Script

Этот скрипт позволяет отправлять эфир (ETH) на несколько адресов в сети Sepolia (тестовая сеть Ethereum) за один запуск. Он включает функции для:
- Подключения к сети Ethereum.
- Подготовки и отправки транзакций.
- Оценки комиссии газа для каждой транзакции.
- Проверки статуса транзакции.
- Записи хешей успешных и неуспешных транзакций в файл.

## Описание работы

1. Скрипт подключается к сети Sepolia через RPC-сервер (например, https://1rpc.io/sepolia).
2. Получает баланс отправителя и информацию о комиссионных сборах для каждой транзакции.
3. Проходит по списку получателей, отправляет эфир на каждый адрес и проверяет статус транзакции.
4. Записывает хеши транзакций в файл `tx_hashes.txt` и адреса неуспешных транзакций в файл `failed_addresses.txt`.
5. В отчете выводится информация о количестве отправленных транзакций, общей сумме отправленного эфира, и балансе отправителя после завершения.

## Особенности

- **Поддержка нескольких получателей**: Скрипт отправляет эфир на несколько адресов, указанных в текстовом файле `recipients.txt`.
- **Оценка комиссии газа**: Используется метод `estimate_gas` для расчета необходимого газа с добавлением 5% для повышения вероятности успешной транзакции.
- **Отчетность**: В конце работы выводится отчет о количестве транзакций, общей сумме эфира, списке неудачных транзакций и остатке на кошельке отправителя.

## Структура проекта

- ├── multi_send_sepolia_eth.py # Основной скрипт 
- ├── recipients.txt # Файл с адресами получателей 
- ├── tx_hashes.txt # Хеши успешных транзакций 
- ├── failed_addresses.txt # Адреса неудачных транзакций
- ├── .env # Файл с приватным ключом и адресом отправителя

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/yourusername/multi-send-eth.git

## Установите зависимости:
pip install -r requirements.txt

## Создайте файл .env в корневой папке проекта и добавьте в него следующие переменные:

PRIVATE_KEY=<ваш_приватный_ключ>
SENDER_ADDRESS=<ваш_адрес_отправителя>

## Убедитесь, что у вас есть файл recipients.txt с адресами получателей. Адреса должны быть записаны по одному в каждой строке.



