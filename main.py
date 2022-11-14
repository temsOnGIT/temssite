#V 1.1 pywebio
import asyncio
import datetime
import os,json
now = datetime.datetime.now()
import pywebio
from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio.session import defer_call, info as session_info, run_async, run_js

chat_msgs = []
online_users = set()
MAX_MESSAGES_COUNT = 100





def users_():
    print(f'{online_users}')



async def main():
    global chat_msgs

    put_markdown("## ✨ Чат от tems#3500!\nV 1.1")
    msg_box = output()

    put_scrollable(msg_box, height=300, keep_bottom=True)


    # def write_name():
    #         online_users.add(nickname)


    bad_nick = ['📢']
    def add_score(nickname: int, amount: int):
        if os.path.isfile("users.json"):
            with open("users.json", "r") as fp:
                data = json.load(fp)
            try:
                data[f"{nickname}"]["password"] = amount
            except KeyError: # if the user isn't in the file, do the following
                data[f"{nickname}"] = {"password": amount} # add other things you want to store
        else:
            data = {f"{nickname}": {"password": amount} }
        # saving the file outside of the if statements saves us having to write it twice
        with open("users.json", "w+") as fp:
            json.dump(data, fp, sort_keys=True, indent=4) # kwargs for beautification
       # you can also return the new/updated score here if you want
    def admin(nickname: int, amount: int):
        if os.path.isfile("users.json"):
            with open("users.json", "r") as fp:
                data = json.load(fp)
            try:
                data[f"{nickname}"]["admin"] = amount
            except KeyError: # if the user isn't in the file, do the following
                data[f"{nickname}"] = {"admin": amount} # add other things you want to store
        else:
            data = {f"{nickname}": {"admin": amount} }
        # saving the file outside of the if statements saves us having to write it twice
        with open("users.json", "w+") as fp:
            json.dump(data, fp, sort_keys=True, indent=4) # kwargs for beautification
       # you can also return the new/updated score here if you want
    def getpass(nickname: int):
        with open("users.json", "r") as fp:
            data = json.load(fp)
        return data[f"{nickname}"]["password"]
    def getadmin(nickname: int):
        with open("users.json", "r") as fp:
            data = json.load(fp)
        return data[f"{nickname}"]["admin"]
    data1 = await input_group(f"👻 Авторизация", [

       actions(name="cmd", buttons=["Войти","Регистрация"])

    ],validate=lambda m: ('msg', "Введите текст сообщения!") if m["cmd"] == "Отправить" and not m['msg'] else None)

    if data1['cmd'] == 'Регистрация':
        nickname = await input("Введите никнейм", required=True, placeholder="Никнейм", validate=lambda n: "❌ Данный пользователь уже зарегистрированн!" if n in online_users or n in bad_nick else None)
        password = await input("Введите пароль", required=True, placeholder="Пароль")
        password1 = await input("Повторите пароль", required=True, placeholder="Пароль")
        if password1 == password:
            add_score(nickname, password)
            admin(nickname, 'False')

    nickname = await input("Войти в чат", required=True, placeholder="Никнейм", validate=lambda n: "❌ Данный пользователь уже в сети!" if n in online_users or n in bad_nick else None)
    password = await input("Войти в чат", required=True, placeholder="Пароль")
    aspassword = getpass(nickname)


    if password == aspassword:

        online_users.add(nickname)


    chat_msgs.append((f'`{now.strftime("%H:%M")}`', f'`{nickname}` присоединился к чату!'))  # internet image)# internet image
    msg_box.append(put_markdown(f'`{now.strftime("%H:%M")}` `{nickname}` присоединился к чату!'))
        #now.strftime("%H:%M")
    refresh_task = run_async(refresh_msg(nickname, msg_box))
    while True:
        admin = getadmin(nickname)
        if admin == 'False':

            data = await input_group(f"✔ {nickname} \n💭 Новое сообщение", [
                input(placeholder="Текст сообщения ...", name="msg"),
                actions(name="cmd", buttons=["Отправить", '👍','😂', '😋','🥱','😘','😫',
                                             '😇','🤡','😱','🙄',
                                             '❤','😰','😑','😬'])
            ],validate=lambda m: ('msg', "Введите текст сообщения!") if m["cmd"] == "Отправить" and not m['msg'] else None)
        if admin == 'True':

            data = await input_group(f"✔ {nickname} \n💭 Новое сообщение", [
                input(placeholder="Текст сообщения ...", name="msg"),
                actions(name="cmd", buttons=["Отправить", "Востановить пароль",'Добавить админа'])
            ],validate=lambda m: ('msg', "Введите текст сообщения!") if m["cmd"] == "Отправить" and not m['msg'] else None)

        if data is None:
            break
        if data['cmd'] =="Востановить пароль":


            data = await input_group(f"✔ {nickname} \n💭 Востановление", [
                input(placeholder="Никнейм", name="nick"),
                input(placeholder="Новый пароль", name="pass"),
                actions(name="cmd", buttons=["Поменять", "Назад"])
            ],validate=lambda m: ('msg', "Введите текст сообщения!") if m["cmd"] == "Отправить" and not m['msg'] else None)
            if data['cmd'] == "Поменять":
                add_score(data['nick'], data['pass'])

            if data['cmd'] == "Назад":
                data = await input_group(f"✔ {nickname} \n💭 Новое сообщение", [
                input(placeholder="Текст сообщения ...", name="msg"),
                actions(name="cmd", buttons=["Отправить", "Востановить пароль",'Добавить админа'])
                ],validate=lambda m: ('msg', "Введите текст сообщения!") if m["cmd"] == "Отправить" and not m['msg'] else None)
        if data['cmd'] =="Добавить админа":


            data = await input_group(f"✔ {nickname} \n💭 Добавить админа", [
                input(placeholder="Никнейм", name="nick"),
                input(placeholder="Ваш пароль", name="pass"),
                actions(name="cmd", buttons=["Добавить", "Назад"])
            ],validate=lambda m: ('msg', "Введите текст сообщения!") if m["cmd"] == "Отправить" and not m['msg'] else None)
            if data['cmd'] == "Добавить":
                if aspassword == password:
                    admin(data['nick'], 'True')

            if data['cmd'] == "Назад":
                data = await input_group(f"✔ {nickname} \n💭 Новое сообщение", [
                input(placeholder="Текст сообщения ...", name="msg"),
                actions(name="cmd", buttons=["Отправить", "Востановить пароль",'Добавить админа'])
                ],validate=lambda m: ('msg', "Введите текст сообщения!") if m["cmd"] == "Отправить" and not m['msg'] else None)

        if data['cmd'] == '😑':
            data['msg']='😑'
        if data['cmd'] == '😬':
            data['msg']='😬'
        if data['cmd'] == '🙄':
            data['msg']='🙄'
        if data['cmd'] == '❤':
            data['msg']='❤'
        if data['cmd'] == '😰':
            data['msg']='😰'
        if data['cmd'] == '😂':
            data['msg']='😂'
        if data['cmd'] == '😋':
            data['msg']='😋'
        if data['cmd'] == '🥱':
            data['msg']='🥱'
        if data['cmd'] == '😘':
            data['msg']='😘'
        if data['cmd'] == '😫':
            data['msg']='😫'
        if data['cmd'] == '😇':
            data['msg']='😇'
        if data['cmd'] == '😱':
            data['msg']='😱'
        if data['cmd'] == '🤡':
            data['msg']='🤡'
        if data['cmd'] == '👍':
            data['msg']='👍'
        msg_box.append(put_markdown(f"`{nickname}` {data['msg']}"))
        print(f"{nickname} {data['msg']}")
        time_message = f'{now.strftime("%H:%M")}'
        chat_msgs.append((nickname, data['msg']))
    refresh_task.close()

    online_users.remove(nickname)
    toast("Вы вышли из чата!")
    msg_box.append(put_markdown(f'📢 Пользователь `{nickname}` покинул чат!'))
    chat_msgs.append(('📢', f'Пользователь `{nickname}` покинул чат!'))

    put_buttons(['Перезайти'], onclick=lambda btn: run_js('window.location.reload()'))


async def refresh_msg(nickname, msg_box):
    global chat_msgs
    last_idx = len(chat_msgs)

    while True:
        await asyncio.sleep(1)

        for m in chat_msgs[last_idx:]:
            if m[0] != nickname:  # if not a message from current user
                msg_box.append(put_markdown(f"`{m[0]}` {m[1]}"))

        # remove expired
        if len(chat_msgs) > MAX_MESSAGES_COUNT:
            chat_msgs = chat_msgs[len(chat_msgs) // 2:]

        last_idx = len(chat_msgs)



if __name__ == "__main__":
    pywebio.platform.django.start_server(main, port=8080, host='', cdn=True, static_dir=None,
                                        remote_access=False, allowed_origins=None, check_origin=None, session_expire_seconds=None,
                                         session_cleanup_interval=None, debug=False, max_payload_size='200M')
