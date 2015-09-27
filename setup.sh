# RethinkDB binary
echo "[Installing RethinkDB] ..."
source /etc/lsb-release && echo "deb http://download.rethinkdb.com/apt $DISTRIB_CODENAME main" | sudo tee /etc/apt/sources.list.d/rethinkdb.list
wget -qO- http://download.rethinkdb.com/apt/pubkey.gpg | sudo apt-key add -
sudo apt-get update
sudo apt-get install rethinkdb
echo "[Installed RethinkDB]"

# lxml dependecies
echo "[Installing lxml dependecies] ..."
sudo apt-get install libxml2-dev libxslt-dev
echo "[Installed lxml dependecies]"

# PIL dependecies
echo "[Installing PIL dependecies] ..."
sudo apt-get install libjpeg-dev zlib1g-dev libpng12-dev
echo "[Installed PIL dependecies]"

# NewsPaper library
echo "[Installing NewsPaper] ..."
sudo pip install newspaper
echo "[Installed RethinkDB]"

# Corpus used for NLP operations
echo "[Downloading NLP Corpus] ..."
curl https://raw.githubusercontent.com/codelucas/newspaper/master/download_corpora.py | python
echo "[Downloaded NLP Corpus]"