import os
import datetime
from zipfile import ZipFile


BACKUP_DIR_NAME = (
    "/home/apidemokoweio/django-demo-mysql/mysql_backups"  # Backup files directory
)
FILE_PREFIX = "db_backup_"  # Prefix of the file that will be generated
FILE_SUFFIX_DATE_FORMAT = "%Y%m%d%H%M%S"  # Date format
USERNAME = "username"  # Your PythonAnywhere username
DB_NAME = USERNAME + "$dbname"  # The MySQL database name
DB_HOST = USERNAME + ".mysql.pythonanywhere-services.com"
# Get today's date and time
timestamp = datetime.datetime.now().strftime(FILE_SUFFIX_DATE_FORMAT)
# Generate the file name
backup_filename = BACKUP_DIR_NAME + "/" + FILE_PREFIX + "_" + timestamp + ".sql"
# Run the MySQL dump to create an image of your MySQL DB
os.system(
    "mysqldump -u"
    + USERNAME
    + " -h "
    + DB_HOST
    + "--set-gtid-purged=OFF --no-tablespaces --column-statistics=0"
    + DB_NAME
    + ">"
    + backup_filename
)

# Zipping the DB image
zip_filename = BACKUP_DIR_NAME + "/" + FILE_PREFIX + timestamp + ".zip"
with ZipFile(zip_filename, "w") as zip:
    zip.write(backup_filename, os.path.basename(backup_filename))

# Remove the backup file (and leave the zipped version)
os.remove(backup_filename)

# List all available zipped database images
list_files = os.listdir(BACKUP_DIR_NAME)

# How many days do we want the backup to stay in our directory
DAYS_TO_KEEP_BACKUP = 4
back_date = datetime.datetime.now() - datetime.timedelta(days=DAYS_TO_KEEP_BACKUP)
back_date = back_date.strftime(FILE_SUFFIX_DATE_FORMAT)

# Deleting files older than DAYS_TO_KEEP_BACKUP days
length = len(FILE_PREFIX)
for f in list_files:
    filename = f.split(".")[0]
    if "zip" == f.split(".")[1]:
        suffix = filename[length:]
        if suffix < back_date:
            print("Deleting file : " + f)
            os.remove(BACKUP_DIR_NAME + "/" + f)
