# PyrogramPaginator
A module for Pyrogram to paginate long messages simply!

### How do I use it?
1. Place the `paginator.py` file in the project path
2. Place this line `paginator = Pagination()` at the beginning of your main code and then insert the following code snippet into the main code
```python
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
```
3. Call it anywhere in the code :)
```python
paginator.__init__(page_count=page_count, text=pages_dict_or_text)
```
- `page_count` is the number of pages you want to be divided.
- The `text` parameter accepts two types of data,
  `dict` and `str`. You can customarily use the dictionary key as the page number and the dictionary value as the text of that page.<br>
  Otherwise, the text is automatically divided into pages of 100 words each.
### What if I have buttons?
You can use 
