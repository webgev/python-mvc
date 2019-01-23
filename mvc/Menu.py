from controllers import controllers

menu = []
def get_menu():
    if menu:
        return menu
    for name in controllers:
        if hasattr(controllers[name], "menu_name"):
            _name = name[:-10].lower()
            _id = _name
            href = "/" if _name == 'home' else "/" + _name
            menu.append((href, _id, str(controllers[name].menu_name)))

    return menu
