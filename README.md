# telegram-support-bot

Other languages: [русский](README.ru.md), english

A telegram bot made in Python that will allow you to quickly deploy a convenient, multifunctional and extensible way to organize technical support for your product via Telegram.

- [Deploy](#deploy)
- [Configuration description](#configuration-description)

## Deploy


Ways:

1. [Deploy using Docker](#deploy-using-docker) (This way is recommended in case you are not going to change the source code)
2. [Deploy using the source code](#deploy-using-the-source-code)

### Deploy using Docker

---

Requirements: Docker (Installation: [Windows](https://docs.docker.com/desktop/install/windows-install/), [Linux](https://docs.docker.com/desktop/install/windows-install/)), [Git](https://git-scm.com/downloads)

First, let's clone this repo using next command:

```
git clone https://github.com/Kamilfo-Developer/telegram-support-bot.git
```

Then go to the repo root directory:

```
cd telegram-support-bot
```

Now we are ready to create `.env` file which will be a config for the app. After it's done, we need to open it using a text editor. For example, [nano](https://www.nano-editor.org/download.php) for Linux or Notepad for Windows.

Since it's done, we have to set bot's configuration. If you launch the app via docker-compose (it's recommended if no additional options needed), simply add to the `.env` file next lines:

```
BOT_TOKEN=<Your bot's token>
OWNER_PASSWORD=<Password for the owner initialization>
```

If you are curious about some of these fields, you can figure out their purpose [here](#configuration-description).

Next, you are going to need Docker. When it's installed, enter next command to the terminal:

```
docker-compose up -d
```

If you've done everything right, the bot will be ready to use. Congratulations!

### Deploy using the source code

---

Requirements: [Python](https://www.python.org/downloads/) of version 3.10 or greater, [Git](https://git-scm.com/downloads)

First, let's clone the repo:

```
git clone https://github.com/Kamilfo-Developer/telegram-support-bot.git
```

Then go to the repo root directory:

```
cd telegram-support-bot
```

Now we have to create `venv`:

- Windows: `python -m venv venv`
- Linux: `python3 -m venv venv`

That far, we are ready to install all the dependencies.

First, let's activate `venv`:

- Windows: `./venv/Scripts/activate`
- Linux: `source venv/bin/activate`

After activating `venv`, we need to install all the packages using pip (the installation speed can vary depending on your device's internet connection quality):

```
pip install -r requirements/prod.txt
```

Now we are ready to create `.env` file which will be a config for the app. After it's done, we need to open it using a text editor. For example, [nano](https://www.nano-editor.org/download.php) for Linux or Notepad for Windows.

Since it's done, we have to set bot's configuration. If you are fine with SQLite as the Database, it's enough to add next lines to the `.env` file:

```
BOT_TOKEN=<Your bot's token>
OWNER_PASSWORD=<Password for the owner initialization>
```

If you are curious about some of these fields, you can figure out their purpose [here](#configuration-description).

After completing the app's configuration, you have to apply migrations for the database using [Alembic](https://alembic.sqlalchemy.org/en/latest/). To do so, enter next commands:

First, go to the migrations directory:

```
cd bot/db/migrations
```

Then apply the migrations:

```
alembic upgrade head
```

Finally, get back to the repo's root directory.

```
cd ../../..
```

If the migrations were applied successfully, you are ready to start the bot. Just use next command:

```
python -m bot
```

If you've done everything right, the bot will be ready to use. Congratulations!

## Configuration description


- [Basic configuration](#basic-configuration)
  1. [BOT_TOKEN](#bot_token)
  2. [OWNER_PASSWORD](#owner_password)
  3. [OWNER_DEFAULT_DESCRIPTIVE_NAME](#owner_default_descriptive_name)
  4. [DEFAULT_LANGUAGE_CODE](#default_language_code)
  5. [DB_PROVIDER](#db_provider)
- [PostgreSQL configuration](#postgresql-configuration)
  1. [POSTGRES_DRIVER_NAME](#postgres_driver_name)
  2. [POSTGRES_DB_NAME](#postgres_db_name)
  3. [POSTGRES_USERNAME](#postgres_username)
  4. [POSTGRES_HOST](#postgres_host)
  5. [POSTGRES_PORT](#postgres_port)
  6. [POSTGRES_PASSWORD](#postgres_password)
- [MySQL configuration](#mysql-configuration)
  1. [MYSQL_DRIVER_NAME](#mysql_driver_name)
  2. [MYSQL_DB_NAME](#mysql_db_name)
  3. [MYSQL_USERNAME](#mysql_username)
  4. [MYSQL_HOST](#mysql_host)
  5. [MYSQL_PORT](#mysql_port)
  6. [MYSQL_PASSWORD](#mysql_password)

<br/>

### **Basic configuration**

---

#### **BOT_TOKEN**

Used for passing the token to the bot. The token can be obtained here: https://telegram.me/BotFather.

**Default value:**: no default value

#### **OWNER_PASSWORD**

Password to for the owner initializing precess. Should be a single world. For example, `MyReallyReliablePassword`.
After starting the bot, you will need to enter `/initowner` command with the password as first argument. Eventually, you will have next string: `/initowner MyReallyReliablePassword`. After sending this comnad, the bot will be ready to use.

**Default value:**: no default value

#### **OWNER_DEFAULT_DESCRIPTIVE_NAME**

Default owner's name. Must be a single word. For example, `OwnerOfThisBot`.

**Default value:**: `Owner`

#### **DEFAULT_LANGUAGE_CODE**

Sets the default language. Will be used if user's language can't be found among the available languages. The string must be a [IETF-tag](https://en.wikipedia.org/wiki/IETF_language_tag#List_of_common_primary_language_subtags). For example, `ru` or `en`.

**Default value:**: `en`.

#### **DB_PROVIDER**

Sets the database, which will be used as bot's storage.
Accepts next values: `sqlite`, `postgres`, `mysql`

**Default value:** `sqlite`

**docker-compose default value:** `postgres`

<br/>

### **PostgreSQL configuration**

---

#### **POSTGRES_DRIVER_NAME**

A name of corresponding asynchronous [SQLAlchemy supported](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#module-sqlalchemy.dialects.postgresql.asyncpg) driver for PostgreSQL.

Keep in mind that for using not default driver, it must be installed first.

**Default value**: `asyncpg`

#### **POSTGRES_DB_NAME**

The name of database inside PostgreSQL.

**Default value**: `postgres`

#### **POSTGRES_USERNAME**

The username inside PostgreSQL.

**Default value**: `postgres`

#### **POSTGRES_HOST**

PostgreSQL database host.

**Default value**: `localhost`

**docker-compose default value:** `db`

#### **POSTGRES_PORT**

PostgreSQL host's port.

**Default value**: `5432`

#### **POSTGRES_PASSWORD**

PostgreSQL user's password.

**Default value**: `postgres`

### MySQL configuration

#### **MYSQL_DRIVER_NAME**

A name of corresponding asynchronous [SQLAlchemy supported](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#module-sqlalchemy.dialects.postgresql.asyncpg) driver for MySQL.

Keep in mind that for using not default driver, it must be installed first.

**Default value**: `asyncmy`

#### **MYSQL_DB_NAME**

The name of database inside PostgreSQL. Must be set if you are using this database.

**Default value**: no default value

#### **MYSQL_USERNAME**

The username inside MySQL. Must be set if you are using this database.

**Default value**: no default value

#### **MYSQL_HOST**

MySQL database host.

**Default value**: `localhost`

#### **MYSQL_PORT**

MYSQL host's port.

**Default value**: `3306`

#### **MYSQL_PASSWORD**

MySQL user's password. Must be set if you are using this database.

**Default value**: no default value
