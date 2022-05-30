# backend-111406

## 專案環境

- 程式語言：Python
- 版本：Python 3.9.8
- 框架：Flask 2.0.3
- ORM：MongoEngine 0.24.1

## 專案設定

1. 啟動CMD or Terminal並切換至專案根目錄
2. 分別輸入以下指令

(in Windows)

```cmd=
python -m venv .venv
.venv\Scripts\activate.bat
```

(in Unix or MacOS)

```terminal=
python -m venv .venv
source .venv/bin/activate
```

3. 接著輸入`pip install -r requirements.txt`以下載所需套件
4. 將`application.py`內的配置檔調整為開發模式

```python=
app.config.from_object('config.Config')
```

## 專案啟動

- CMD、Terminal
    1. 切換目錄至專案根目錄
    2. 輸入`python application.py`
- google app engine
    1. 切換目錄至專案根目錄
    2. 確認`application.py`內之DB連線字串
    3. 輸入`gcloud app deploy`, 接著輸入`Y`

## 專案負責人員

|  姓名  |         信箱         |
|:------:|:--------------------:|
| 林哲立 | 10846006@ntub.edu.tw |