from nicegui import ui, app
import side_bar
from chat_area import CreateChatArea
from ai import initialize_model_stream, loadModel
from utils import Loading
from backend import get_messages, create_chat

@ui.page('/')
async def page():
    AI_BLUE = {
        "primary": "#2563EB",     
        "secondary": "#F8FAFC",   
        "background": "#FFFFFF",  
        "surface": "#EEF2FF",     
        "text": "#0F172A",        
        "muted_text": "#64748B",  
        "accent": "#22D3EE",      
        "border": "#CBD5E1",      
        "btn-secondary": "#60A5FA",
        "chat-bg": "#F8FAFF",
        "ai-msg": "#EEF2FF",
        "ai-msg-text": "#0F172A",
        "user-msg": "#2563EB",
        "user-msg-text": "#FFFFFF",
        "ai-border": "#CBD5E1",
        "user-border": "#1D4ED8",
        "ai-msg-active": "#E0F7FF",
    }
    ui.colors(**AI_BLUE)
    await ui.context.client.connected()
    async def LoadModel():
        loading = Loading("Loading Models...")
        _ = await loadModel() #type:ignore
        loading.delete()
        return _

    def openChat(id, models, lister):
        chat_area.clear()
        msgs = get_messages(id)
        if len(msgs) > 10:
            msgs = msgs[-10:]
        assistant = initialize_model_stream(**models, msgs=msgs)
        with chat_area: CreateChatArea(id, assistant, lister)

    def createChat(models, lister):
        chat_area.clear()
        created_chat = create_chat()
        assistant = initialize_model_stream(**models, msgs=[])
        with chat_area: CreateChatArea(created_chat['id'], assistant, lister)

    await side_bar.Create_Side_Bar(createChat, openChat, LoadModel)
    chat_area = ui.element().classes("w-full h-full flex")

# app.on_disconnect(lambda: [app.shutdown(), exit()])
ui.run(reload=True, native=True)