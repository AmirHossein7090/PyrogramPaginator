# Your imports ...
from paginator import Pagination  # Don't forget this!

app = Client(name='my_app')

# -- Add this line to your code --
paginator = Pagination()

# -- Add this function to your codes --
@app.on_callback_query(filters.regex(r'^page#\d{1}$'))
async def paginator_callback(client, callback_query):
    chat_id: int = callback_query.from_user.id
    message_id: int = callback_query.message.id
    page_number: int = int(callback_query.data.split('#')[-1])
    paginator.current_page = page_number
    try:
        await client.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=paginator.display(page_number),
            reply_markup=paginator.markup,
            disable_web_page_preview=True,
        )
    except pyrogram.errors.MessageNotModified:
        pass  # Ignore current page callback

async def job(client, callback_query):
    buttons = [[InlineKeyboardButton('Back', callback_data='back')]]
    # ...
    paginator.__init__(page_count=page_count, text=pages_dict_or_text)  # Call it anywhere in the code :)
  
    # Add buttons after paginator buttons
    paginator.add_after(buttons)
    # Or add buttons before paginator buttons
    paginator.add_before(buttons)
