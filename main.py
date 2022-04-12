########## KanaKy_0.9.3.6 ##########

from datetime import date, datetime
start_time = datetime.today()

from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty, ObjectProperty, ListProperty

from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior
from kivymd.uix.list import OneLineListItem
from kivymd.uix.list import OneLineIconListItem, MDList
from kivymd.uix.list import ThreeLineIconListItem

from kivymd.uix.tab import MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.boxlayout import MDBoxLayout

from kivymd.icon_definitions import md_icons
from kivymd.font_definitions import fonts
from kivymd import images_path

from kivymd.uix.picker import MDDatePicker
from kivymd.uix.dialog import MDDialog

from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp

from kivymd.uix.list import ThreeLineIconListItem
from kivy.uix.screenmanager import ScreenManager, Screen

from kivy.clock import Clock
from kivy.core.window import Window

from kivymd.uix.snackbar import Snackbar
from kivymd.uix.spinner import MDSpinner

import sqlite3
#from pydocxtpl import DocxWriter
import random

Window.softinput_mode = "below_target"

tovar = [[], [], [], [], [], [], [], [], [], []]
tovar_eng = ["vodka", "cognac", "liquor", "low_alcohol", "wine", "beer", "k_beer", "water", "coffee", "other"]

try:
    conn = sqlite3.connect('tovar.db')
    cur = conn.cursor()

    for k in range(10):
        cur.execute(f"SELECT * from {tovar_eng[k]}")
        records = cur.fetchall()
        for row in records:
            tovar[k].append(list(row))

    cur.execute("SELECT * from contacti")
    records = cur.fetchall()
    contacti = []
    for pos in records:
        contacti.append(list(pos))

    cur.close()
    
except sqlite3.Error as error:
    Snackbar(text = "Ошибка работы базы данных").open()
finally:
    if (conn):
        conn.close()

tovar_rus = ["Водка", "Коньяк", "Ликёр", "Слабоалкоголка", "Вино", "Пиво", "к Пиву", "Вода,Сок", "Кофе", "Прочее"]
tovar_content = ['content_vodka', 'content_cognac', 'content_liquor', 'content_low_alcohol', 'content_wine', 'content_beer', 'content_k_beer', 'content_water', 'content_coffee', 'content_other']
itogo_tovar = ['itogo_vodka', 'itogo_cognac', 'itogo_liquor', 'itogo_low_alcohol', 'itogo_wine', 'itogo_beer', 'itogo_k_beer', 'itogo_water', 'itogo_coffee', 'itogo_other']
tovar_summa = ['vodka_summa', 'cognac_summa', 'liquor_summa', 'low_alcohol_summa', 'wine_summa', 'beer_summa', 'k_beer_summa', 'water_summa', 'coffee_summa', 'other_summa']

itogo = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
del_tovar = [0, 0]
del_postavshik = 0
flag_spisok = [1, 1, 1]

bills_nom = [1000, 500, 200, 100, 50, 20, 10, 5, 2, 1, 10, 5, 2, 1, 0.5, 0.1]
bills_col = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

class Tab(MDFloatLayout):
    pass

class ContentNavigationDrawer(MDBoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()

class IconListItem(OneLineIconListItem):
    icon = StringProperty()
 
class ContentTovar(BoxLayout):
    naz = StringProperty()
    cena = StringProperty()
    tvod = StringProperty()
    ind = ObjectProperty()

class Content_Price(BoxLayout):
    price_naz = StringProperty()
    price_cena = StringProperty()
    price_ind = NumericProperty()
    color = ListProperty()

class Content_Postavka(ThreeLineIconListItem):
    cont_org = StringProperty()
    cont_name = StringProperty()
    cont_phone1 = StringProperty()
    cont_ind = NumericProperty()

class KanaKy(MDApp):
    color_toolbar = "#006F50"
    color_tab = "#006F50"
    color_bar = "#006F50"
    color_title = "#000000"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_file('interface.kv')
        
    def build(self):
        return self.screen

    def on_save_date(self, instance, value, date_range):
        val = value.strftime("%d.%m.%Y")
        self.screen.ids.start_date.text = f"{val}"

    def on_cancel_date(self, instance, value):
        '''Events called when the "CANCEL" dialog box button is clicked.'''
        
    def date_dialog(self):
        date_dialog = MDDatePicker(min_year = 2021, max_year = 2030)
        date_dialog.bind(on_save=self.on_save_date, on_cancel=self.on_cancel_date)
        date_dialog.open()

    def set_item(self, text_item):
        self.screen.ids.barmen.text = text_item
        self.menu_barmen.dismiss()

    def on_start(self):
        menu_items = [
            {
                "viewclass": "IconListItem",
                "height": dp(56),
                "icon": "account-arrow-right-outline",
                "text": "Оксана -> Алина",
                "on_release": lambda x=f"Оксана -> Алина": self.set_item(x),}, 
            {
                "viewclass": "IconListItem",
                "height": dp(56), 
                "icon": "account-arrow-right-outline",
                "text": "Алина -> Оксана",
                "on_release": lambda x=f"Алина -> Оксана": self.set_item(x),}]
        self.menu_barmen = MDDropdownMenu(
            caller=self.screen.ids.barmen,
            items=menu_items,
            position="bottom",
            width_mult=4,)
        self.menu_barmen.bind()
        self.screen.ids.start_date.text = f'{date.today().strftime("%d.%m.%Y")}'
        self.dialog = MDDialog(text = f"Время запуска: {datetime.today() - start_time}",)
        self.dialog.open()

    def start_tovar(self):
        start_time = datetime.today()
        global flag_spisok
        if flag_spisok[0] == 0:
            return
        else:  
            for k in range(0, len(tovar)):
                self.root.ids[f"{tovar_content[k]}"].clear_widgets()
                for i in range(0, len(tovar[k])):
                    self.root.ids[f"{tovar_content[k]}"].add_widget(
                        ContentTovar(naz = f"{tovar[k][i][0]}", cena = f"{tovar[k][i][3]}", tvod=f"{tovar[k][i][1]}", ind = k))
        flag_spisok[0] = 0
        MDDialog(text = f"Время запуска: {datetime.today() - start_time}",).open()

    def calc_tovar(self, values):
        itogo[values] = 0
        try:
            for i in range(0, len(tovar[values])):
                k = len(tovar[values])-i-1
                tovar[values][i][1] = self.root.ids[tovar_content[values]].children[k].ids.tovar_field.text
                tovar[values][i][2] = float(round(eval(tovar[values][i][1]), 3))
                tovar[values][i][3] = self.root.ids[tovar_content[values]].children[k].ids.tovar_cena.text
                tovar[values][i][4] = float(round((tovar[values][i][2]*float(tovar[values][i][3])), 3))
                self.root.ids[tovar_content[values]].children[k].ids.tovar_sum.text = f'{tovar[values][i][4]} грн'
                itogo[values] += tovar[values][i][4]  
                if tovar[values][i][7] == 'шт.':
                    tovar[values][i][2] = int(tovar[values][i][2])
                self.root.ids[tovar_content[values]].children[k].ids.tovar_col.text = f'{tovar[values][i][2]}{tovar[values][i][7]} по '
            self.root.ids[itogo_tovar[values]].text = f'{itogo[values]}грн.'
            self.root.ids[tovar_summa[values]].text = f'{itogo[values]}грн.'
        except Exception:
            Snackbar(text = "ошибка ввода данных").open()
        finally:
            for i in range(0, len(tovar[values])):
                self.root.ids[tovar_content[values]].children[i].ids.tovar_field.text = self.root.ids[tovar_content[values]].children[i].ids.tovar_field.text.replace(',', '.')
                if self.root.ids[tovar_content[values]].children[i].ids.tovar_field.text == '':
                    self.root.ids[tovar_content[values]].children[i].ids.tovar_field.text = '0'
                    Snackbar(text = "не указано количество товара, обнулино").open()
                elif len(self.root.ids[tovar_content[values]].children[i].ids.tovar_field.text)>1 and self.root.ids[tovar_content[values]].children[i].ids.tovar_field.text[0]=="0" and self.root.ids[tovar_content[values]].children[i].ids.tovar_field.text[1]!=".":
                    self.root.ids[tovar_content[values]].children[i].ids.tovar_field.text = self.root.ids[tovar_content[values]].children[i].ids.tovar_field.text[1:]
                    Snackbar(text = "первым символом был 0, обрезали").open()
                elif self.root.ids[tovar_content[values]].children[i].ids.tovar_cena.text == '':
                    self.root.ids[tovar_content[values]].children[i].ids.tovar_cena.text = '0'
                    Snackbar(text = "не указана цена, обнулено").open()

    def calc_itogo(self):
        self.root.ids.itogo_summa.text = f'{sum(itogo)}грн.'

    def on_menu_right(self):
        pass

        # tovar_docx = ['vod', 'cog', 'liq', 'low', 'wine', 'beer', 'k_beer', 'wat', 'cof', 'oth']
        # context = {
            # 'title': f'{self.screen.ids.barmen.text}',
            # 'data': f'{self.screen.ids.start_date.text}',
            # 'ito_sum': f'{sum(itogo)}'}
        # for k in range(len(tovar_docx)):
            # context[f"sum_{tovar_docx[k]}"] = f'{itogo[k]}'
            # for i in range(len(tovar[k])):
                # context[f"{tovar_docx[k]}_naz{i}"] = tovar[k][i][0]
                # context[f"{tovar_docx[k]}{i}"] = tovar[k][i][1]
                # context[f"{tovar_docx[k]}_col{i}"] = tovar[k][i][2]
                # context[f"{tovar_docx[k]}_cena{i}"] = tovar[k][i][3]
                # context[f"{tovar_docx[k]}_sum{i}"] = tovar[k][i][4]
        # mydoc = DocxWriter("shablon.docx")
        # mydoc.render(context)
        # mydoc.save(f"/storage/emulated/0/doc{self.screen.ids.start_date.text}.docx")
        # self.dialog = MDDialog(title = "ВЫПОЛНЕНО:", text = f"файл doc{self.screen.ids.start_date.text}.docx сохранен", radius=[20, 20, 20, 20], type='custom')
        # self.dialog.open()

    def cena_update_query(self, price_list, par):
        try:
            conn = sqlite3.connect('tovar.db')
            cur = conn.cursor()
            print("Подключен к SQLite для смены цен")
            print(par, price_list)
            for i in range(10):
                if par==i:
                    sqlite_update_query = f"Update vodka set cena = ? where id = ?"
                    break
            cur.executemany(sqlite_update_query, price_list)
            conn.commit()
            cur.close()
            Snackbar(text = "цены обновлены").open()
            
        except sqlite3.Error as error:
            self.dialog = MDDialog(title = "ОШИБКА:", text = "проблема в работе с базой данных",)
            self.dialog.open()
        finally:
            if conn:
                conn.close()
            
    def cena_update(self, par):
        price_list = []
        for i in range(0, len(tovar[par])):
            price_list.append((self.root.ids[tovar_content[par]].children[i].ids.tovar_cena.text, tovar[par][len(tovar[par])-i-1][5]))
        self.cena_update_query(price_list, par)

    def col_vo_update_query(self, col_vo_list, par):
        try:
            conn = sqlite3.connect('tovar.db')
            cur = conn.cursor()
            for i in range(10):
                if par==i:
                    sqlite_update_query = f"Update {tovar_eng[i]} set stroka = ? where id = ?"
                    break
            cur.executemany(sqlite_update_query, col_vo_list)
            conn.commit()
            cur.close()
            Snackbar(text = "кол-во обновлено").open()

        except sqlite3.Error as error:
            self.dialog = MDDialog(title = "ОШИБКА:", text = "проблема в работе с базой данных",)
            self.dialog.open()
        finally:
            if conn:
                conn.close()
            
    def col_vo_update(self, par):
        col_vo_list = []
        for i in range(0, len(tovar[par])):
            col_vo_list.append((self.root.ids[tovar_content[par]].children[i].ids.tovar_field.text, tovar[par][len(tovar[par])-i-1][5]))
        self.col_vo_update_query(col_vo_list, par)

    def calc_bills(self):
        for i in range(0, 16):
            if self.root.ids[f"bills{i}"].text == '':
                bills_col[i] = 0
            else:
                bills_col[i] = int(self.root.ids[f"bills{i}"].text)
            bills_col[i] = bills_col[i] * bills_nom[i]
        self.root.ids.itogo_bills.text = f'{sum(bills_col)}грн.'
        
    def clean_bills(self):
        for i in range(0, 16):
            self.root.ids[f'bills{i}'].text = ''
        self.calc_bills()

    def on_start_tovar(self):
        global flag_spisok
        if flag_spisok[1] == 0:
            return
        else:  
            self.price_list(del_tovar[0])
            menu_items_price = [
                {
                    "text": f"{tovar_rus[i]}",
                    "viewclass": "OneLineListItem",
                    "on_release": lambda index_kat=i, x=f"{tovar_rus[i]}": self.menu_choice(index_kat, x),
                } for i in range(10)]
            self.menu_price = MDDropdownMenu(
                caller=self.screen.ids.kategoria,
                items=menu_items_price,
                width_mult=4,)
            self.menu_price.bind()
        flag_spisok[1] = 0

    def menu_choice(self, index_kat, text_item):
        self.screen.ids.kategoria.text = text_item
        self.menu_price.dismiss()
        del_tovar[0] = index_kat
        self.price_list(index_kat)

    def price_list(self, index_kat):
        self.root.ids.cont_price.clear_widgets()
        for i in range(0, len(tovar[index_kat])):
            row_color = (0.2, 0.2, 0.2, 0.2)
            if (i%2 != 0):
                row_color = (1, 1, 1, 1)
            self.root.ids.cont_price.add_widget(
                Content_Price(
                    price_naz = f'{tovar[index_kat][i][0]}',
                    price_cena = f'{int(float(tovar[index_kat][i][3])*float(tovar[index_kat][i][6])+0.1)} за {tovar[index_kat][i][6]}{tovar[index_kat][i][7]}',
                    price_ind = i,
                    color = row_color))

    def new_tov_clean(self):
        self.root.ids.newtov_toolbar.title = "Новый товар"
        self.root.ids.newtov_naz.text = ''
        self.root.ids.newtov_cena.text = '0'
        self.root.ids.newtov_size.text = '1'
        self.root.ids.newtov_unit.text = 'л.'
        self.root.ids.newtov_col.text = '0'
        self.root.ids.newtov_del.disabled = True
        self.root.ids.newtov_edit.disabled = True
        self.root.ids.newtov_new.disabled = False
        self.root.ids.screen_manager_tovar.current = "tovar_input"
        self.root.ids.screen_manager_tovar.transition.direction = "left"

    def new_tovar_create(self):
        global flag_spisok
        flag_spisok[1] = 1
        flag_spisok[0] = 1
        cont_list_id = []
        for i in range(0, len(tovar[del_tovar[0]])):
            cont_list_id.append(tovar[del_tovar[0]][i][5])
        if len(cont_list_id) == 0: cont_id = 10000
        else: cont_id = max(cont_list_id)+1

        tovar[del_tovar[0]].append([
            self.root.ids.newtov_naz.text,
            self.root.ids.newtov_col.text,
            0,
            float(self.root.ids.newtov_cena.text)/float(self.root.ids.newtov_size.text),
            0,
            cont_id,
            self.root.ids.newtov_size.text,
            self.root.ids.newtov_unit.text,])
        cont = (
            self.root.ids.newtov_naz.text,
            self.root.ids.newtov_col.text,
            float(self.root.ids.newtov_cena.text)/float(self.root.ids.newtov_size.text),
            cont_id,
            self.root.ids.newtov_size.text,
            self.root.ids.newtov_unit.text,)
        for i in range(10):
            if del_tovar[0]==i:
                sqlite_insert_query = f"INSERT INTO {tovar_eng[i]} (naz, stroka, cena, id, size, unit) VALUES (?, ?, ?, ?, ?, ?);"
                break
        self.sqlitedb(sqlite_insert_query, cont, 0)
        Snackbar(text = "добавлена одна позиция").open()
        self.on_start_tovar()

    def upgrade_tov_price(self, number_tovar):
        global del_tovar
        del_tovar[1] = number_tovar
        self.root.ids.newtov_toolbar.title = "Изменить товар"
        self.root.ids.newtov_naz.text = tovar[del_tovar[0]][del_tovar[1]][0]
        self.root.ids.newtov_cena.text = str(int(float(tovar[del_tovar[0]][del_tovar[1]][3])*float(tovar[del_tovar[0]][del_tovar[1]][6])+0.1))
        self.root.ids.newtov_size.text = str(tovar[del_tovar[0]][del_tovar[1]][6])
        self.root.ids.newtov_unit.text = tovar[del_tovar[0]][del_tovar[1]][7]
        self.root.ids.newtov_col.text = str(tovar[del_tovar[0]][del_tovar[1]][1])
        self.root.ids.newtov_del.disabled = False
        self.root.ids.newtov_edit.disabled = False
        self.root.ids.newtov_new.disabled = True
        self.root.ids.screen_manager_tovar.current = "tovar_input"
        self.root.ids.screen_manager_tovar.transition.direction = "left"

    def upgrade_tov_create(self):
        global flag_spisok
        flag_spisok[1] = 1
        flag_spisok[0] = 1
        tovar[del_tovar[0]][del_tovar[1]] = [
            self.root.ids.newtov_naz.text,
            self.root.ids.newtov_col.text,
            0,
            float(self.root.ids.newtov_cena.text)/float(self.root.ids.newtov_size.text),
            0,
            tovar[del_tovar[0]][del_tovar[1]][5],
            self.root.ids.newtov_size.text,
            self.root.ids.newtov_unit.text,]
        cont = (
            self.root.ids.newtov_naz.text,
            self.root.ids.newtov_col.text,
            float(self.root.ids.newtov_cena.text)/float(self.root.ids.newtov_size.text),
            self.root.ids.newtov_size.text,
            self.root.ids.newtov_unit.text,
            tovar[del_tovar[0]][del_tovar[1]][5],)
        for i in range(10):
            if del_tovar[0]==i:
                sqlite_insert_query = f"Update {tovar_eng[i]} set naz = ?, stroka = ?, cena = ?, size = ?, unit = ? where id = ?"
                break
        self.sqlitedb(sqlite_insert_query, cont, 0)
        Snackbar(text = "изменена одна позиция").open()
        self.on_start_tovar()

    def delete_tov(self):
        global flag_spisok
        flag_spisok[1] = 1
        flag_spisok[0] = 1
        cont = (tovar[del_tovar[0]][del_tovar[1]][5], )
        tovar[del_tovar[0]].pop(del_tovar[1])
        for i in range(10):
            if del_tovar[0]==i:
                sqlite_insert_query = f"DELETE from {tovar_eng[i]} where id = ?"
                break
        self.sqlitedb(sqlite_insert_query, cont, 0)
        Snackbar(text = "удалена одна позиция").open()
        self.on_start_tovar()

    def on_start_postavshik(self):
        global flag_spisok
        if flag_spisok[2] == 0:
            return
        else:  
            self.root.ids.con_post.clear_widgets()
            for i in range(0, len(contacti)):
                self.root.ids.con_post.add_widget(
                    Content_Postavka(
                        cont_org = contacti[i][1],
                        cont_name = contacti[i][2],
                        cont_phone1 = contacti[i][3],
                        cont_ind = i))
        flag_spisok[2] = 0

    def new_post_clean(self):
        self.root.ids.post_toolbar.title = "Новый поставщик"
        self.root.ids.post_org.text = ''
        self.root.ids.post_account.text = ''
        self.root.ids.post_number_phone1.text = ''
        self.root.ids.post_number_phone2.text = ''
        self.root.ids.post_note.text = ''
        self.root.ids.post_del.disabled = True
        self.root.ids.post_edit.disabled = True
        self.root.ids.post_new.disabled = False
        self.root.ids.screen_manager_post.current = "postav_input"
        self.root.ids.screen_manager_post.transition.direction = "left"

    def new_postavshik(self):
        global flag_spisok
        flag_spisok[2] = 1
        cont_list_id = []
        for i in range(0, len(contacti)):
            cont_list_id.append(contacti[i][0])
        if len(cont_list_id) == 0: cont_id = 1000
        else: cont_id = max(cont_list_id)+1
        contacti.append([
            cont_id,
            self.root.ids.post_org.text,
            self.root.ids.post_account.text,
            self.root.ids.post_number_phone1.text,
            self.root.ids.post_number_phone2.text,
            self.root.ids.post_note.text,])
        sqlite_insert_query = """INSERT INTO contacti
                                (id, org, name, number1, number2, note)
                                VALUES (?, ?, ?, ?, ?, ?);"""
        cont = (
            cont_id,
            self.root.ids.post_org.text,
            self.root.ids.post_account.text,
            self.root.ids.post_number_phone1.text,
            self.root.ids.post_number_phone2.text,
            self.root.ids.post_note.text,)
        self.sqlitedb(sqlite_insert_query, cont, 0)
        Snackbar(text = "добавлен один контакт").open()
        self.on_start_postavshik()

    def upgrade_cont(self, number_cont):
        global del_postavshik
        del_postavshik = number_cont
        self.root.ids.post_toolbar.title = "Изменить данные"
        self.root.ids.post_org.text = contacti[del_postavshik][1]
        self.root.ids.post_account.text = contacti[del_postavshik][2]
        self.root.ids.post_number_phone1.text = contacti[del_postavshik][3]
        self.root.ids.post_number_phone2.text = contacti[del_postavshik][4]
        self.root.ids.post_note.text = contacti[del_postavshik][5]
        self.root.ids.post_del.disabled = False
        self.root.ids.post_edit.disabled = False
        self.root.ids.post_new.disabled = True
        self.root.ids.screen_manager_post.current = "postav_input"
        self.root.ids.screen_manager_post.transition.direction = "left"

    def upgrade_postavshik(self):
        global flag_spisok
        flag_spisok[2] = 1
        contacti[del_postavshik] = [
            contacti[del_postavshik][0],
            self.root.ids.post_org.text,
            self.root.ids.post_account.text,
            self.root.ids.post_number_phone1.text,
            self.root.ids.post_number_phone2.text,
            self.root.ids.post_note.text,]
        sqlite_insert_query = """Update contacti set 
                                org = ?, name = ?, number1 = ?, number2 = ?, note = ? 
                                where id = ?"""
        cont = (
            self.root.ids.post_org.text,
            self.root.ids.post_account.text,
            self.root.ids.post_number_phone1.text,
            self.root.ids.post_number_phone2.text,
            self.root.ids.post_note.text,
            contacti[del_postavshik][0])
        self.sqlitedb(sqlite_insert_query, cont, 0)
        Snackbar(text = "изменён один контакт").open()
        self.on_start_postavshik()

    def delete_postavshik(self):
        global flag_spisok
        flag_spisok[2] = 1
        sqlite_insert_query = """DELETE from contacti where id = ?"""
        cont = (contacti[del_postavshik][0], )
        contacti.pop(del_postavshik)
        self.sqlitedb(sqlite_insert_query, cont, 0)
        Snackbar(text = "удалён один контакт").open()
        self.on_start_postavshik()

    def omore_random(self):
        more_id = random.randint(0, 100)
        try:
            conn = sqlite3.connect('tovar.db')
            cur = conn.cursor()
            sql_select = """SELECT * from omore where id = ?"""
            cur.execute(sql_select, (more_id,))
            records = cur.fetchall()
            for row in records:
                self.root.ids.lab_more.text = row[1]
            cur.close()
        except sqlite3.Error as error:
            Snackbar(text = "ошибка при работе с SQLite").open()
        finally:
            if (conn):
                conn.close()

    def sqlitedb(self, sqlite_insert_query, content_list, index):
        try:
            conn = sqlite3.connect('tovar.db')
            cur = conn.cursor()

            cur.execute(sqlite_insert_query, content_list)
            conn.commit()
            cur.close()

        except sqlite3.Error as error:
            Snackbar(text = "ошибка при работе с SQLite").open()
        finally:
            if conn:
                conn.close()

KanaKy().run()