from pynput import keyboard

# def on_press(key):
#     if key == keyboard.Key.f7
#
# keyboard.Listener(on_press=on_press).run()aa

# COMBINATION = { keyboard.Key.ctrl,'q' }
#
# # The currently active modifiers
# current = set()
#
#
# def on_press(key):
#     if key in COMBINATION:
#         current.add(key)
#         if all(k in current for k in COMBINATION):
#             print('All modifiers active!')
#     if key == keyboard.Key.esc:
#         listener.stop()
#
#
# def on_release(key):
#     try:
#         current.remove(key)
#     except KeyError:
#         pass
#
#
# with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
#     listener.join()


# def on_activate():
#     print('Global hotkey activated!')
#
# def for_canonical(f):
#     return lambda k: f(l.canonical(k))
#
# hotkey = keyboard.HotKey(
#     keyboard.HotKey.parse('<ctrl>+]'),
#     on_activate)
# with keyboard.Listener(
#         on_press=for_canonical(hotkey.press),
#         on_release=for_canonical(hotkey.release)) as l:
#     l.join()

# listener = keyboard.Listener(on_press=for_canonical(hotkey.press), on_release=for_canonical(hotkey.release),suppress=True)
# listener.start()


account = []
account.append('user')
account.append('password')
print((account))