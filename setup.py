from subprocess import call
import os, sys

currdir = os.path.dirname(__file__)
call([sys.executable,"-m","pip","install","-r",os.path.join(currdir, "requirements.txt")])

if os.name == "posix":
    mecabname = "mecab-python3"
else:
    mecabname = "mecab"

call([sys.executable,"-m","pip","install",mecabname])

if "nltk_data" not in os.listdir(os.getenv("APPDATA")):
    import nltk
    nltk.download("punkt")
