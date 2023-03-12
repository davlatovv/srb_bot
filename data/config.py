import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))

admins = os.getenv("ADMIN_ID").split(",")

allowed_users = [

]

PG_USER = str(os.getenv("PGUSER"))
PG_PASS = str(os.getenv("PGPASSWORD"))
DATABASE = str(os.getenv("DATABASE"))
PGHOST = str(os.getenv("PGHOST"))
PM_TOKEN = str(os.getenv("PAYME_TOKEN"))
BOT_NICKNAME = str(os.getenv("BOT_NICKNAME"))
ADMIN_NICK = str(os.getenv("ADMIN_NICK"))

POSTGRES_URI = f"postgresql://{PG_USER}:{PG_PASS}@{PGHOST}/{DATABASE}"

I18N_DOMAIN = "schoolbot"
BASE_DIR = Path(__file__).parent.parent
LOCALES_DIR = BASE_DIR / 'locales'

monthly_amount = 25000000
daily_amount = 1000000