import os
import shutil


def clean_database():
    if os.path.exists("database"):
        shutil.rmtree("database")
    os.makedirs("database")
