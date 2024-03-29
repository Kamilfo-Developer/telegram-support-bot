# telegram-support-bot

Версия данного файла доступна на следующих языках: русский, [english](README.md)

Телеграм-бот, написанный на языке Python, который позволит Вам в кратчайшие сроки развернуть удобный, многофункциональный и расширяемый способ организации технической поддержки Вашего продукта через Telegram.

- [Запуск](#запуск)
- [Описание конфигурации](#описание-конфигурации)

## Запуск

Способы:

1. [Запуск через Docker](#запуск-с-помощью-docker) (Данный способ рекомендован в случае, если Вам не требуется дополнительных опций при запуске бота)
2. [Запуск бота с помощью исходного кода](#запуск-с-помощью-исходного-кода)

### Запуск через Docker

---

Требования: Docker (Установка: [Windows](https://docs.docker.com/desktop/install/windows-install/), [Linux](https://docs.docker.com/desktop/install/windows-install/)), [Git](https://git-scm.com/downloads)

Склонируем данный репозиторий репозиторий с помощью следующей команды:

```
git clone https://github.com/Kamilfo-Developer/telegram-support-bot.git
```

Перейдём в папку с исходным кодом репозитория:

```
cd telegram-support-bot
```

Теперь создадим файл `.env` с конфигурацией приложения. После создания его необходимо открыть, используя текстовый редактор. Например, [nano](https://www.nano-editor.org/download.php) на Linux или Notepad (Блокнот) на Windows.

После чего следует задать конфигурацию бота. Если Вы запускаете приложение через docker-compose (рекомендуется, если Вы хотите запустить обычную версию бота), то добавьте в файл `.env` следующие строчки:

```
BOT_TOKEN=<Токен Вашего бота>
OWNER_PASSWORD=<Пароль для инициализации владельца бота>
DEFAULT_LANGUAGE_CODE=ru
```

Если Вам непонятны назначения полей данного файла, их описание можно посмотреть [здесь](#описание-конфигурации).

На следующем этапе нам понадобится Docker. После его установки, введите следующую команду:

```
docker-compose up -d
```

Если Вы сделали всё верно, то бот запустится и будет готов к использованию. Поздравляем!

### Запуск с помощью исходного кода

---

Требования: [Python](https://www.python.org/downloads/) версии не менее 3.10, [Git](https://git-scm.com/downloads)

Для начала склонируем репозиторий:

```
git clone https://github.com/Kamilfo-Developer/telegram-support-bot.git
```

После чего откроем директорию с исходным кодом:

```
cd telegram-support-bot
```

Здесь нам понадобится установить `poetry`:

- Для Windows: `pip install poetry`
- Для Linux: `pip3 install poetry`

Теперь можно установить зависимости. Для этого достаточно ввести следующую команду (скорость установки зависит от скорости подключения Вашего устройства):

```
poetry install
```

После чего активируем среду с установленными зависимостями:

```
poetry shell
```

Теперь создадим файл `.env` с конфигурацией приложения. После создания его необходимо открыть, используя текстовый редактор. Например, [nano](https://www.nano-editor.org/download.php) на Linux или Notepad (Блокнот) на Windows.

После чего следует задать конфигурацию бота. Если в качестве базы данных Вам будет достаточно SQLite и в качестве языка по умолчанию будет выступать русский, то Вам достаточно добавить в файл `.env` следующие строчки:

```
BOT_TOKEN=<Токен Вашего бота>
OWNER_PASSWORD=<Пароль для инициализации владельца бота>
DEFAULT_LANGUAGE_CODE=ru
```

Если Вам непонятны назначения полей данного файла, их описание можно посмотреть [здесь](#описание-конфигурации).

После конфигурации приложения необходимо сделать миграции с помощью [Alembic](https://alembic.sqlalchemy.org/en/latest/). Для этого введите следующие команды:

Сначала перейдите в дерикторию с миграциями:

```
cd bot/db/migrations
```

Затем выполните сами миграции:

```
alembic upgrade head
```

После чего вернитесь в корневую папку репозитория

```
cd ../../..
```

Если всё прошло успешно, то можно запускать бота. Для этого необходимо ввести:

```
python -m bot
```

Если Вы сделали всё верно, то бот запустится и будет готов к использованию. Поздравляем!

## Описание конфигурации

- [Основная конфигурация](#основная-конфигурация)
  1. [BOT_TOKEN](#bot_token)
  2. [OWNER_PASSWORD](#owner_password)
  3. [OWNER_DEFAULT_DESCRIPTIVE_NAME](#owner_default_descriptive_name)
  4. [DEFAULT_LANGUAGE_CODE](#default_language_code)
  5. [DB_PROVIDER](#db_provider)
- [Конфигурация PostgreSQL](#конфигурация-postgresql)
  1. [POSTGRES_DRIVER_NAME](#postgres_driver_name)
  2. [POSTGRES_DB_NAME](#postgres_db_name)
  3. [POSTGRES_USERNAME](#postgres_username)
  4. [POSTGRES_HOST](#postgres_host)
  5. [POSTGRES_PORT](#postgres_port)
  6. [POSTGRES_PASSWORD](#postgres_password)
- [Конфигурация MySQL](#конфигурация-mysql)
  1. [MYSQL_DRIVER_NAME](#mysql_driver_name)
  2. [MYSQL_DB_NAME](#mysql_db_name)
  3. [MYSQL_USERNAME](#mysql_username)
  4. [MYSQL_HOST](#mysql_host)
  5. [MYSQL_PORT](#mysql_port)
  6. [MYSQL_PASSWORD](#mysql_password)

<br/>

### **Основная конфигурация**

---

#### **BOT_TOKEN**

Используется для указания токена бота. Токен можно здесь: https://telegram.me/BotFather.

**Значение по умолчанию**: отсутствует

#### **OWNER_PASSWORD**

Пароль для инициализации владельца бота. Должен состоять из одного слова, например: `МойОченьНадёжныйПароль`. После запуска бота, необходимо будет ввести команду `/initowner`, в качестве аргумента передав пароль. В итоге получится строка: `/initowner МойОченьНадёжныйПароль`. После отправки данной команды боту он будет готов к использованию.

**Значение по умолчанию**: отсутствует

#### **OWNER_DEFAULT_DESCRIPTIVE_NAME**

Имя владельца по умолчанию. Должно состоять из одного слова. Например, `ВладелецДанногоБота`.

**Значение по умолчанию**: `Owner`

#### **DEFAULT_LANGUAGE_CODE**

Задаёт язык по умолчанию. Он будет использован, если среди поддерживаемых ботом языков не нашлось пользовательского. Строка с указанным языком должна соответствовать [IETF-тегу](https://en.wikipedia.org/wiki/IETF_language_tag#List_of_common_primary_language_subtags). Например, `ru` или `en`.

**Значение по умолчанию**: `en`.

#### **DB_PROVIDER**

Задаёт используемую базу данных.
Может принимать следующие значения: `sqlite`, `postgres`, `mysql`

**Значение по умолчанию:** `sqlite`

**Значение по умолчанию в docker-compose:** `postgres`

#### **TIMEZONE**

Часовой пояс, который будет использован при форматировании сообщений для пользователей. Пример: `Europe/Moscow`. Полный список в подобном формате может быть найден [здесь](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List).

**Значение по умолчанию:** будет использован локальный часовой пояс

<br/>

### **Конфигурация PostgreSQL**

---

#### **POSTGRES_DRIVER_NAME**

Название соответствующего асинхронного драйвера для PostgreSQL, [поддерживаемого SQLAlchemy](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#module-sqlalchemy.dialects.postgresql.asyncpg).

Имейте в виду, что при использовании драйвера не по умолчанию, его сначала придётся установить.

**Значение по умолчанию**: `asyncpg`

#### **POSTGRES_DB_NAME**

Название используемой базы данных внутри PostgreSQL.

**Значение по умолчанию**: `postgres`

#### **POSTGRES_USERNAME**

Имя пользователя внутри PostgreSQL.

**Значение по умолчанию**: `postgres`

#### **POSTGRES_HOST**

Хост базы данных PostgreSQL.

**Значение по умолчанию**: `localhost`

**Значение по умолчанию в docker-compose:** `db`

#### **POSTGRES_PORT**

Значение порта для базы данных PostgreSQL.

**Значение по умолчанию**: `5432`

#### **POSTGRES_PASSWORD**

Пароль для базы данных PostgreSQL.

**Значение по умолчанию**: `postgres`

### Конфигурация MySQL

#### **MYSQL_DRIVER_NAME**

Название соответствующего асинхронного драйвера для PostgreSQL, [поддерживаемого SQLAlchemy](https://docs.sqlalchemy.org/en/20/dialects/mysql.html#module-sqlalchemy.dialects.mysql.asyncmy).

Имейте в виду, что при использовании драйвера не по умолчанию, его сначала придётся установить.

**Значение по умолчанию**: `asyncmy`

#### **MYSQL_DB_NAME**

Название используемой базы данных внутри MySQL. При использовании соответствующей БД, должно быть задано.

**Значение по умолчанию**: отсутствует

#### **MYSQL_USERNAME**

Имя пользователя внутри MySQL. При использовании соответствующей БД, должно быть задано.

**Значение по умолчанию**: отcутствует

#### **MYSQL_HOST**

Хост базы данных MySQL.

**Значение по умолчанию**: `localhost`

#### **MYSQL_PORT**

Значение порта для базы данных MYSQL.

**Значение по умолчанию**: `3306`

#### **MYSQL_PASSWORD**

Пароль для базы данных MySQL. При использовании соответствующей БД, должно быть задано.

**Значение по умолчанию**: отсутствует
