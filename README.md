Installation
---
---
Download ChromeDriver https://sites.google.com/a/chromium.org/chromedriver/downloads

Rename `.env.sample` to `.env`
and define missing settings there.

```
$ pip install -r requirements.txt
```

#Run
```
$ python main.py -q '"python developer" AND "Minsk"' -p '30' -x '159.203.84.241:3128'
```
or
```
$ python main.py -query '"python developer" AND "Minsk"' -page '30' -proxy '159.203.84.241:3128'
```
Proxy is an optional argument.