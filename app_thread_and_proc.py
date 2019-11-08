from os import getenv
from dotenv import load_dotenv
from requests import get as GET
from multiprocessing.pool import Pool
from multiprocessing.dummy import Pool as ThreadPool

LOAD = 5
ID = 10_128_449


def main():
    pool = ThreadPool(processes=LOAD)
    results = []
    for i in range(ID, ID + LOAD):
        results.append(pool.apply_async(func=call_api, args=[i]))
    pool.close()
    pool.join()

    pool = Pool(processes=LOAD)
    for i in results:
        pool.apply_async(func=save_as_pdf, args=[i.get()['id'], i.get()['content']])
    pool.close()
    pool.join()


def call_api(id):
    try:
        return {'id': id, 'content': GET(f"{getenv('URL_WEB_SERVICE')}{id}").content}
    except Exception as e:
        return e


def save_as_pdf(name, content):
    with open(f"{name}.pdf", 'wb') as f:
        f.write(content)


if __name__ == "__main__":
    load_dotenv()
    main()
