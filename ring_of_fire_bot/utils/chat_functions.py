from functools import wraps

from telegram import Chat, ChatMember, Bot, Update


def is_user_admin(chat: Chat, user_id: int, member: ChatMember = None) -> bool:
    if chat.type == 'private' \
            or chat.all_members_are_administrators:
        return True

    if not member:
        member = chat.get_member(user_id)
    return member.status in ('administrator', 'creator')


def user_admin(func):
    @wraps(func)
    def is_admin(bot: Bot, update: Update, *args, **kwargs):
        user = update.effective_user
        if user and is_user_admin(update.effective_chat, user.id):
            return func(bot, update, *args, **kwargs)

        elif not user:
            pass

        else:
            update.effective_message.reply_text("Only an admin can perform this task")

    return is_admin
