# Programming vacancies compare

The script analyzes vacancies on the job search sites [HeadHunter](https://www.hh.ru/) and [SuperJob](https://www.superjob.ru/) and shows the average salary for several popular programming languages. The script uses the [HeadHunter](https://dev.hh.ru/) and [SuperJob](https://dev.hh.ru/) API to get data.

## Prerequisites

Python3 should be already installed. Use `pip` to install dependencies:
```bash
pip install -r requirements.txt
```

## Installation
You have to set SUPERJOB_API_KEY environment variables before use script.

1. Create .env file in project directory.
2. Visit [SuperJob API portal](https://api.superjob.ru/), sign up and get Secret Key. Copy your Secret Key to .env file:
```
export SUPERJOB_API_KEY="v3.r.999999999.6435bca22222cd7ad4f1d731bf8b270bc91c130e.10722d661b4111111eaaecac34f9361defed5f6f"
```

## Usage

Run python script:
```sh
python main.py
```
The data will be output to the terminal.

## Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).

## Meta

Vitaly Klyukin — [@delphython](https://t.me/delphython) — [delphython@gmail.com](mailto:delphython@gmail.com)

[https://github.com/delphython](https://github.com/delphython/)
