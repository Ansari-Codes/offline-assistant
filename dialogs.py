from UI import Dialog, confirm, Label, Button, Input, Select, Card, Row, Col, Slider
from backend import write_config, read_config

def createSettings():
    settings_dialog = Dialog()
    settings_dialog.props('persistent')
    config = read_config()
    edited = config.copy()
    with settings_dialog, Card().classes("w-full h-fit max-w-[90vw] max-h-[90vh] sm:max-w-[50vw] sm:max-h-[50vh]"):
        with Col().classes("w-full"):
            with Row().classes("w-full"):
                Label("Temperature").classes("w-fit font-bold text-lg")
                Slider(0.1, 2, 0.1, onchange=lambda e: edited.update({"temperature": float(e.value)})).props('label-always').classes("flex flex-1").set_value(config.get("temperature"))
            with Row().classes("w-full"):
                Label("Top P").classes("w-fit font-bold text-lg")
                Slider(0.1, 1, 0.1, onchange=lambda e: edited.update({"top_p": float(e.value)})).props('label-always').classes("flex flex-1").set_value(config.get("top_p"))
            with Row().classes("w-full"):
                Label("Max New Tokens").classes("w-fit font-bold text-lg")
                Slider(128, 8000, 1, onchange=lambda e: edited.update({"max_new_tokens": int(e.value)})).props('label-always').classes("flex flex-1").set_value(config.get("max_new_tokens"))
        def save():
            config.update(edited)
            write_config(edited)
            settings_dialog.delete()
        with Row().classes("w-full justify-end"):
            Button("Cancel", settings_dialog.delete, color='negative')
            Button("Save", save)
    return settings_dialog
