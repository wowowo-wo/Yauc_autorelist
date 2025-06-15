# Yauc_autorelist

This is a python tool that automatically relist closed auctions on Yahoo! Auctions using Selenium (without Yahoo official API).

## Using

### 1. Install Google Chrome (on Ubuntu):

```bash
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/google-chrome.gpg
echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | sudo tee /etc/apt/sources.list.d/google-chrome.list
sudo apt update
sudo apt install google-chrome-stable
```

### 2. Install ChromeDriver matching your Chrome version:

check your installed Chrome version and install the corresponding ChromeDriver via pip

```bash
google-chrome --version
# ex: xxx.x.xxxx.xxx
pip install chromedriver-py==xxx.x.xxxx.xxx # Replace xxx.x.xxxx.xxx with your actual Chrome version from the above command.
```

### 3. Clone this repo and install requirements:

```bash
git clone https://github.com/wowowo-wo/Yauction_auto_relist
cd Yauction_auto_relist
pip install -r requirements.txt
```

### 4. Log in to Yahoo! Auctions

run the login script to authenticate your Yahoo! account:

```bash
python3 login.py
```

### 5. Relist closed auctions

once logged in, run the script to relist closed auctions:

```bash
python3 relist.py
```

## Requirements

selenium
chromedriver-py (installed manually as shown above)