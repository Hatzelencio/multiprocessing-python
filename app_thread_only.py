from os import getenv
from dotenv import load_dotenv
from requests import get as GET
from multiprocessing.dummy import Pool as ThreadPool

LOAD = 5
ID = 10_128_449


def main():
    lll = list(range(ID, ID + LOAD))
    pool = ThreadPool(processes=len(lll))
    results = []
    for i in lll:
        results.append(pool.apply_async(func=call_api, args=[i]))
    pool.close()
    pool.join()

def call_api(id):
    try:
        save_as_pdf(id, GET(f"{getenv('URL_WEB_SERVICE')}{id}").content)
        return True
    except Exception as e:
        return e


def save_as_pdf(name, content):
    with open(f"{name}.pdf", 'wb') as f:
        f.write(content)


if __name__ == "__main__":
    load_dotenv()
    main()
