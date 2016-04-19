# RethinkDB binary
echo "[Installing RethinkDB server binary] ..."
source /etc/lsb-release && echo "deb http://download.rethinkdb.com/apt $DISTRIB_CODENAME main" | sudo tee /etc/apt/sources.list.d/rethinkdb.list
wget -qO- http://download.rethinkdb.com/apt/pubkey.gpg | sudo apt-key add -
sudo apt-get update
sudo apt-get install rethinkdb

# RethinkDB client
echo "[Installing RethinkDB client library] ..."
sudo pip install rethinkdb

# lxml dependecies
echo "[Installing lxml dependecies] ..."
sudo apt-get install libxml2-dev libxslt-dev

# PIL dependecies
echo "[Installing PIL dependecies] ..."
sudo apt-get install libjpeg-dev zlib1g-dev libpng12-dev

# NewsPaper library
echo "[Installing NewsPaper] ..."
sudo pip install newspaper

# Corpus used for NLP operations
echo "[Downloading NLP Corpus] ..."
curl https://raw.githubusercontent.com/codelucas/newspaper/master/download_corpora.py | python

echo "[Installing the gnustep-gui-runtime]"
sudo apt-get install -y gnustep-gui-runtime

echo "Installing necessary libraries"
sudo pip install -U -r requirements.txt 