from pystray import Icon as icon, Menu as menu, MenuItem as item

state = False

def on_clicked(icon, item):
    global state
    state = not item.checked

# Update the state in `on_clicked` and return the new state in
# a `checked` callable
icon('test', create_image(), menu=menu(
    item(
        'Checkable',
        on_clicked,
        checked=lambda item: state))).run()