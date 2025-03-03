import logging
import threading


def worker(event):
    while not event.isSet():
        logging.debug("рабочий поток вносится")
        event.wait(1)


def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(relativeCreated)6d %(threadName)s %(message)s"
    )
    event = threading.Event()

    thread = threading.Thread(target=worker, args=(event,))
    thread_two = threading.Thread(target=worker, args=(event,))
    thread.start()
    thread_two.start()

    while not event.isSet():
        try:
            logging.debug("Добавление из главного потока")
            event.wait(0.75)
        except KeyboardInterrupt:
            event.set()
            break


if __name__ == "__main__":
    main()
