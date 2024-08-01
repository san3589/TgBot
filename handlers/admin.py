from aiogram import Router
from filters.chat_types import ChatTypeFilter


admin_router = Router()
admin_router.message.filter(ChatTypeFilter(['private']))
