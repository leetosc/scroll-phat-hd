#!/usr/bin/env python

import time
import unicodedata

try:
    import queue
except ImportError:
    import Queue as queue

import scrollphathd
from scrollphathd.fonts import font5x7

try:
    import tweepy
except ImportError:
    tweepy = None

KEYWORD = '#bilgetank'
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET = ''
TEXT_BRIGHTNESS = 0.1
SCROLL_DELAY = 0.02
TWEET_PAUSE = 0.25
EMPTY_QUEUE_SLEEP = 1.0

q = queue.Queue()


def mainloop(stop_event, get_config):
    scrollphathd.clear()
    scrollphathd.show()

    while stop_event is None or not stop_event.is_set():
        try:
            scrollphathd.clear()
            status = q.get(False)
            brightness = get_config("TEXT_BRIGHTNESS", TEXT_BRIGHTNESS)
            status_length = scrollphathd.write_string(
                status, x=0, y=0, font=font5x7, brightness=brightness
            )
            time.sleep(get_config("TWEET_PAUSE", TWEET_PAUSE))

            while status_length > 0:
                if stop_event is not None and stop_event.is_set():
                    return
                scrollphathd.show()
                scrollphathd.scroll(1)
                status_length -= 1
                time.sleep(get_config("SCROLL_DELAY", SCROLL_DELAY))

            scrollphathd.clear()
            scrollphathd.show()
            time.sleep(get_config("TWEET_PAUSE", TWEET_PAUSE))
            q.task_done()

        except queue.Empty:
            time.sleep(get_config("EMPTY_QUEUE_SLEEP", EMPTY_QUEUE_SLEEP))


def run_display(stop_event=None, get_config=None):
    if get_config is None:
        get_config = lambda k, d=None: globals().get(k, d)

    if tweepy is None:
        raise ImportError(
            "This script requires the tweepy module\nInstall with: sudo pip install tweepy"
        )

    consumer_key = get_config("CONSUMER_KEY", CONSUMER_KEY)
    consumer_secret = get_config("CONSUMER_SECRET", CONSUMER_SECRET)
    access_token = get_config("ACCESS_TOKEN", ACCESS_TOKEN)
    access_token_secret = get_config("ACCESS_TOKEN_SECRET", ACCESS_TOKEN_SECRET)

    if not all([consumer_key, consumer_secret, access_token, access_token_secret]):
        raise ValueError(
            "Configure Twitter API keys (CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)"
        )

    class MyStreamListener(tweepy.StreamListener):
        def on_status(self, status):
            if not status.text.startswith('RT'):
                status_text = u'     >>>>>     @{name}: {text}     '.format(
                    name=status.user.screen_name.upper(),
                    text=status.text.upper(),
                )
                try:
                    status_text = unicodedata.normalize('NFKD', status_text).encode('ascii', 'ignore')
                except BaseException as exc:
                    print(exc)

                q.put(status_text)

        def on_error(self, status_code):
            print("Error: {}".format(status_code))
            if status_code == 420:
                return False

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    listener = MyStreamListener()
    stream = tweepy.Stream(auth=api.auth, listener=listener)
    keyword = get_config("KEYWORD", KEYWORD)

    stream.filter(track=[keyword], stall_warnings=True, is_async=True)

    try:
        mainloop(stop_event, get_config)
    finally:
        stream.disconnect()


if __name__ == "__main__":
    if tweepy is None:
        import sys
        sys.exit("This script requires the tweepy module\nInstall with: sudo pip install tweepy")
    try:
        run_display()
    except KeyboardInterrupt:
        scrollphathd.clear()
        scrollphathd.show()
