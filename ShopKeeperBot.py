import telebot
from config import API_TOKEN, channel_cid, admins
from text import *
from telebot.types import ReplyKeyboardMarkup, ReplyKeyboardRemove,InlineKeyboardButton, InlineKeyboardMarkup
from dql import get_category_data
from dml import insert_user_data, insert_sale_data, insert_sale_row_data


bot = telebot.TeleBot(API_TOKEN)
hide_board = ReplyKeyboardRemove()
user_step = dict()  # TO count the user step 
user_basket = dict()  # To store user baskets
temp_products_data = {100 :{}}

def listener(messages):
    for m in messages:
        if m.content_type == 'text':
            print(str(m.chat.first_name) + ' [' + str(m.chat.id) + ']: ' + m.text)
bot.set_update_listener(listener)


@bot.callback_query_handler(func=lambda call: True)
def callback_query_function(call):
    call_id = call.id
    cid = call.message.chat.id
    mid = call.message.message_id
    data = call.data
    print(f'button pressed id : {call_id}, mid : {mid}, cid : {cid}, data : {data}')

    if data.startswith('add'):
        command, code, qty = data.split('_')
        code = int(code)
        qty = int(qty)

        if cid not in user_basket:
            user_basket[cid] = {}
        if code in user_basket[cid]:
            user_basket[cid][code] += qty
        else:
            user_basket[cid][code] = qty

        bot.answer_callback_query(call_id, f'محصول با کد {code} به سبد خرید شما اضافه شد.')
        bot.delete_message(cid, mid)
        bot.send_message(cid, texts['added'])

        # for exporting the basket items to database
        if int(code) == 1:
            insert_sale_data(cid)
            insert_sale_row_data('1', qty)

        elif int(code) == 2:
            insert_sale_data(cid)
            insert_sale_row_data('2', qty)

        elif int(code) == 3:
            insert_sale_data(cid)
            insert_sale_row_data('3', qty)

        elif int(code) == 4:
            insert_sale_data(cid)
            insert_sale_row_data('4', qty)

    elif data.startswith('edit'):
        command, code, qty = data.split('_')
        code = int(code)
        qty = int(qty)
        
        edit_markup = InlineKeyboardMarkup()
        edit_markup.add(InlineKeyboardButton('➖', callback_data=f'change_{code}_{qty-1}'),
                        InlineKeyboardButton(str(qty), callback_data='empty'),
                        InlineKeyboardButton('➕', callback_data=f'change_{code}_{qty+1}'))
        edit_markup.add(InlineKeyboardButton(glass_button['remove'], callback_data=f'remove_{code}'))
        edit_markup.add(InlineKeyboardButton(buttons['back'], callback_data='cancel'))

        bot.edit_message_text(f"ویرایش محصول با کد {code} :", chat_id=cid, message_id=mid, reply_markup=edit_markup)


    elif data.startswith('remove'):
        call_id = call.id
        cid = call.message.chat.id
        data = call.data.split('_')
        code = int(data[1])

        if cid in user_basket and code in user_basket[cid]:
            del user_basket[cid][code]
            bot.answer_callback_query(call_id, f'محصول با کد {code} از سبد خرید شما حذف شد.')
        else:
            bot.answer_callback_query(call_id, 'محصولی با این کد در سبد خرید شما وجود ندارد.')


    elif data.startswith('change'):
        command, code, new_qty = data.split('_')
        if new_qty == '0':
            bot.answer_callback_query(call_id, texts['zero_error'])
        else:
            new_markup = generate_product_markup(int(code), int(new_qty))
            bot.edit_message_reply_markup(cid, mid, reply_markup=new_markup)
            bot.answer_callback_query(call_id, f'تعداد کالا به {new_qty} عدد تغییر یافت')


    elif data == 'cancel':
        bot.delete_message(cid, mid)
        bot.send_message(cid, texts['cancel'])

    '''It's for the admin commands that the admin add a product and chose a category ⬇⬇⬇ '''
    # elif data.startswith('select'):
    # # select_{cat_id}_{new_key}
    # cat_id = int(data.split('_')[1])
    # product_key = int(data.split('_')[-1])
    # product_data = temp_products_data[product_key]
    # res = bot.send_photo(channel_cid, product_data['file_id'], caption=str(product_data))
    # channel_mid = res.message_id
    # insert_product_data(product_data['name'], product_data['description'], cat_id, product_data['price'], product_data['inv'], channel_mid)
    # bot.send_message(cid, 'product added to database successfully')
    # bot.edit_message_reply_markup(cid, mid, reply_markup=None)


@bot.message_handler(commands = ['start'])
def start_command(message):
    cid = message.chat.id
    chat_id = str(message.chat.id)
    name = str(message.chat.first_name)
    user_name = str(message.chat.username)

    if cid in admins:
        role = 'Admin'
        reply_keyboard = ReplyKeyboardMarkup(resize_keyboard = True)
        reply_keyboard.add(buttons['basket'], buttons['products'])
        reply_keyboard.add(buttons['profile'], buttons['help'])
        reply_keyboard.add(buttons['adding'])
        bot.copy_message(cid, channel_cid, message_ids['start_message'], reply_markup = reply_keyboard)
        insert_user_data(chat_id, name, user_name, role)
    else:
        role = 'Customer'
        reply_keyboard = ReplyKeyboardMarkup(resize_keyboard = True)
        reply_keyboard.add(buttons['basket'], buttons['products'])
        reply_keyboard.add(buttons['profile'], buttons['help'])
        bot.copy_message(cid, channel_cid, message_ids['start_message'], reply_markup = reply_keyboard)
        insert_user_data(chat_id, name, user_name, role)


@bot.message_handler(commands=['help'])
@bot.message_handler(func=lambda message: message.text == buttons['help'])
def help_command(message):
    cid = message.chat.id
    bot.copy_message(cid, channel_cid, message_ids['help_text'])


@bot.message_handler(func=lambda m: m.text == (buttons['products']))
def products(message):
    cid = message.chat.id
    # bot.send_message(cid, '', reply_markup = hide_board)
    reply_keyboard = ReplyKeyboardMarkup(resize_keyboard = True)
    reply_keyboard.add(buttons['digital'], buttons['wearing'])
    reply_keyboard.add(buttons['shoes'], buttons['stationery'])
    reply_keyboard.add(buttons['back'])
    bot.copy_message(cid, channel_cid, message_ids['chooseing_cat'], reply_markup = reply_keyboard)
    user_step[cid] = 1


@bot.message_handler(func=lambda m: m.text == (buttons['basket']))
def basket_command(message):
    cid = message.chat.id

    if cid in user_basket and user_basket[cid]:
        basket_contents = "\n".join([f'کد محصول : {code} ، تعداد : {qty}' for code, qty in user_basket[cid].items()])
        response_text = f"محصولات شما در سبد خرید:\n{basket_contents}"
    else:
        response_text = texts['empty_basket']
    
    reply_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    reply_keyboard.add(buttons['payment'], buttons['editing'])
    reply_keyboard.add(buttons['back'])
    bot.send_message(cid, response_text, reply_markup=reply_keyboard)

@bot.message_handler(func=lambda m: m.text == (buttons['profile']))
def profile_command(message):
    cid = message.chat.id
    name = message.chat.first_name
    user_name = message.chat.username

    reply_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    reply_keyboard.add(buttons['back'], buttons['deposit'])
    bot.send_message(cid, f'نام : {name} \n آیدی : @{user_name} \n آیدی عددی : {cid}', reply_markup=reply_keyboard)
    user_step[cid] = 3


@bot.message_handler(func=lambda m: m.text == (buttons['adding']))
def adding_command(message):
    cid = message.chat.id
    if cid in admins:
        bot.copy_message(cid, channel_cid, message_ids['adding_text'])
        user_step[cid] = 4
    else:
        bot.copy_message(cid, channel_cid, message_ids['error'])

def generate_product_markup(code, qty):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('➖' , callback_data = f'change_{code}_{qty-1}'), 
               InlineKeyboardButton(str(qty), callback_data = 'empty'), 
               InlineKeyboardButton('➕' , callback_data = f'change_{code}_{qty+1}'))
    markup.add(InlineKeyboardButton(glass_button['add_to_basket'], callback_data = f'add_{code}_{qty}'))
    markup.add(InlineKeyboardButton(glass_button['cancel'], callback_data = 'cancel'))
    return markup


@bot.message_handler(func=lambda m: user_step.setdefault(m.chat.id, 0)==1)
def user_step_1_handler(message):
    text = message.text
    cid = message.chat.id

    if text == buttons['digital']:

        inline_markup = generate_product_markup(1, 1)
        bot.copy_message(cid, channel_cid, 19, reply_markup = inline_markup)

    elif text == buttons['wearing']:
        inline_markup = generate_product_markup(2, 1)
        bot.copy_message(cid, channel_cid, 20, reply_markup = inline_markup)

    elif text == buttons['shoes']:
        inline_markup = generate_product_markup(3, 1)
        bot.copy_message(cid, channel_cid, 23, reply_markup = inline_markup)
    
    elif text == buttons['stationery']:
        inline_markup = generate_product_markup(4, 1)
        bot.copy_message(cid, channel_cid, 24, reply_markup = inline_markup)
    
    elif text == buttons['back']:
        start_command(message)


@bot.message_handler(func=lambda m: user_step.setdefault(m.chat.id, 0)==2)
def user_step_2_handler(message):
    cid = message.chat.id
    text = message.text
    if text == buttons['payment']:
        bot.send_message(cid, texts['pay'])

    elif text == buttons['back']:
        start_command(message)

    else :
        if cid in user_basket and user_basket[cid]:
            editing_markup = InlineKeyboardMarkup()
            for code, qty in user_basket[cid].items():
                editing_markup.add(
                    InlineKeyboardButton(f'کد محصول: {code}, تعداد: {qty}', callback_data=f'edit_{code}_{qty}')
                )
            editing_markup.add(InlineKeyboardButton(buttons['back'], callback_data='cancel'))
            bot.send_message(cid, texts['chose_edit'], reply_markup=editing_markup)
            
        else:
            bot.send_message(cid, texts['empty_basket'])
        

@bot.message_handler(func=lambda m: user_step.setdefault(m.chat.id, 0)==3)
def user_step_3_handler(message):
    cid = message.chat.id
    text = message.text
    if text == buttons['back']:
        start_command(message)
    elif text == buttons['deposit']:
        bot.send_message(cid, texts['deposit'])


# These tow functions below are the reaction of the bot to the admin command and i don't know why it dosen't work
'''
@bot.message_handler(func=lambda m: user_step.setdefault(m.chat.id, 0)==4)
def user_step_4_handler(message):
    cid = message.chat.id
    if cid in admins:
        photo_id = message.photo[-1].file_id
        caption = message.caption
        items = caption.split('*')
        name = items[0].split(':')[-1].strip()
        desc = items[1].split(':')[-1].strip()
        price = items[2].split(':')[-1].strip()
        inv = items[3].split(':')[-1].strip()
        file_id = message.photo[-1].file_id
        data = {'name': name, 'description': desc, 'price': price, 'inv': inv, 'file_id': file_id}
        new_key = max(temp_products_data.keys()) + 1
        temp_products_data[new_key] = data
        markup = InlineKeyboardMarkup()
        categories = get_category_data()
        for cat in categories:
            cat_id = cat['ID']
            cat_name = cat['name']
            markup.add(InlineKeyboardButton(cat_name, callback_data=f'select_{cat_id}_{new_key}'))
        bot.send_message(cid, f'please select category for product name: {name}', reply_markup=markup)'''

@bot.message_handler(func=lambda m: True, content_types=['photo'])
def photo_message_handle(message):
    cid = message.chat.id
    if cid in admins and user_step.setdefault(cid, 0)==4:
        caption = message.caption
        items = caption.split('*')
        name = items[0].split(':')[-1].strip()
        description = items[1].split(':')[-1].strip()
        price = float(items[2].split(':')[-1].strip())
        inventory = int(items[3].split(':')[-1].strip())
        file_id = message.photo[-1].file_id
        data = {'name': name, 'description': description, 'price': price, 'inv': inventory, 'file_id': file_id}
        new_key = max(temp_products_data.keys()) + 1
        temp_products_data[new_key] = data
        print(data)
        print(temp_products_data)
        markup = InlineKeyboardMarkup()
        categories = get_category_data()
        for cat in categories:
            cat_id = cat['ID']
            cat_name = cat['name']
            markup.add(InlineKeyboardButton(cat_name, callback_data=f'select_{cat_id}_{new_key}'))
        bot.send_message(cid, f'please select category for product name: {name}', reply_markup=markup)
    else:
        bot.copy_message(cid, channel_cid, message_ids['error'])


bot.infinity_polling()