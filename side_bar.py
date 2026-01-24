from UI import Drawer, Button, Col, RawCol, Row, Card, Input, openLink, AddSpace, Label
from backend import all_chats
import env
import utils

async def Create_Side_Bar(chat_creator=None, chat_opener=None, loader=None):
    drawer = Drawer().classes("bg-surface")
    tokenizer, model, tm = await loader() # type:ignore
    def open_chat(chat):
        if chat_opener: 
            chat_opener(chat['id'], dict(model=model, tokenizer=tokenizer))
    def ListChats(e=None):
        query = search.value.lower().strip() # type:ignore
        chats.clear()
        with chats:
            for chat in all_chats(query):
                g20 = len(chat.get('title',''))>20
                print(chat)
                with Button(text=chat.get('title', '')[:g20*20 + (not g20)*len(chat.get('title', ''))] + '...'*g20, on_click=lambda c=chat: open_chat(c))\
                    .props(f'icon="message" color="btn-secondary" align="left"')\
                    .classes(f"w-full"):
                        env.ui.tooltip(f"Last update on {utils.time_ago(chat.get('last_update'))}")\
                .props('anchor="center end" self="center middle"')
    with drawer:
        with RawCol().classes("w-full h-full flex flex-col"):
            with Card().classes("w-full h-fit mb-1 bg-primary"):
                Label(env.LOGO + ' ' + env.NAME).classes("text-2xl font-bold w-full text-white")
            Button(
                'New Chat',
                on_click=chat_creator,
                config={'icon':'add'}
            ).classes("w-full mb-2")

            search = Input(
                placeholder='Search chats...'
            ).classes("w-full mb-1")

            chats = RawCol().classes(
                "gap-1 w-full flex-1 overflow-y-auto mt-1 mb-2 p-0.5 border-1 border-[var(--q-border)] rounded-sm bg-secondary"
            )
            search.on_value_change(ListChats)
            ListChats()
            Button(
                'Settings',
                on_click=lambda: print("Settings"),
                config={'icon': 'settings'}
            ).classes("w-full mb-2")
            Button(
                'About',
                on_click=lambda:(),
                config={'icon':'info'}
            ).classes("w-full mb-2")
    return drawer
