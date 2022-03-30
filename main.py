########## KanaKy_0.9.3 ##########

from datetime import date, datetime
start_time = datetime.today()

from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty, ObjectProperty

from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior
from kivymd.uix.list import OneLineIconListItem, MDList

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

import sqlite3
from docxtpl import DocxTemplate
import random

Window.size = (350, 600)
Window.softinput_mode = "below_target"

#получение данных товара
try:
    conn = sqlite3.connect('tovar.db')
    cur = conn.cursor()
    print("База данных создана и успешно подключена к SQLite")

    # создаём словари для товара
    cur.execute("SELECT * from vodka")
    records = cur.fetchall()
    vodka = []
    for row in records:
        vodka.append(list(row))
    
    cur.execute("SELECT * from cognac")
    records = cur.fetchall()
    cognac = []
    for row in records:
        cognac.append(list(row))
           
    cur.execute("SELECT * from liquor")
    records = cur.fetchall()
    liquor = []
    for row in records:
        liquor.append(list(row))
           
    cur.execute("SELECT * from low_alcohol")
    records = cur.fetchall()
    low_alcohol = []
    for row in records:
        low_alcohol.append(list(row))
           
    cur.execute("SELECT * from wine")
    records = cur.fetchall()
    wine = []
    for row in records:
        wine.append(list(row))
           
    cur.execute("SELECT * from beer")
    records = cur.fetchall()
    beer = []
    for row in records:
        beer.append(list(row))
           
    cur.execute("SELECT * from k_beer")
    records = cur.fetchall()
    k_beer = []
    for row in records:
        k_beer.append(list(row))
           
    cur.execute("SELECT * from water")
    records = cur.fetchall()
    water = []
    for row in records:
        water.append(list(row))
           
    cur.execute("SELECT * from coffee")
    records = cur.fetchall()
    coffee = []
    for row in records:
        coffee.append(list(row))
            
    cur.execute("SELECT * from other")
    records = cur.fetchall()
    other = []
    for row in records:
        other.append(list(row))

    # получение данных о контактах
    cur.execute("SELECT * from contacti")
    records = cur.fetchall()
    contacti = []
    for pos in records:
        contacti.append(list(pos))

    cur.close()
    
except sqlite3.Error as error:
    print("Ошибка при подключении к sqlite", error)
finally:
    if (conn):
        conn.close()
        print("Соединение с SQLite закрыто")

tovar = [vodka, cognac, liquor, low_alcohol, wine, beer, k_beer, water, coffee, other]
tovar_content = ['content_vodka', 'content_cognac', 'content_liquor', 'content_low_alcohol', 'content_wine', 'content_beer', 'content_k_beer', 'content_water', 'content_coffee', 'content_other']
itogo = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

del_postavshik = 0

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
    
class Content_Postavka(ThreeLineIconListItem):
    cont_org = StringProperty()
    cont_name = StringProperty()
    cont_phone1 = StringProperty()
    cont_ind = StringProperty()

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

    # функция даты on_save, on_cancel, date_dialog
    def on_save_date(self, instance, value, date_range):
        val = value.strftime("%d.%m.%Y")
        self.screen.ids.start_date.text = f"{val}"

    def on_cancel_date(self, instance, value):
        '''Events called when the "CANCEL" dialog box button is clicked.'''
        
    def date_dialog(self):
        date_dialog = MDDatePicker(min_year = 2021, max_year = 2030)
        date_dialog.bind(on_save=self.on_save_date, on_cancel=self.on_cancel_date)
        date_dialog.open()
    
    # функция выбора бармена
    def set_item(self, text_item):
        self.screen.ids.barmen.text = text_item
        self.menu.dismiss()
         
################################################################################
#                   функция при запуске                                        #
################################################################################

    def on_start(self):

        # выбор барменов
        menu_items = [
            {
                "viewclass": "IconListItem",
                "height": dp(56),
                "icon": "account-arrow-right-outline",
                "text": "Оксана -> Алина",
                "on_release": lambda x=f"Оксана -> Алина": self.set_item(x),
            }, 
            {
                "viewclass": "IconListItem",
                "height": dp(56), 
                "icon": "account-arrow-right-outline",
                "text": "Алина -> Оксана",
                "on_release": lambda x=f"Алина -> Оксана": self.set_item(x),}]
        self.menu = MDDropdownMenu(
            caller=self.screen.ids.barmen,
            items=menu_items,
            position="bottom",
            width_mult=4,)
        self.menu.bind()

        #дата по умолчанию
        self.screen.ids.start_date.text = f'{date.today().strftime("%d.%m.%Y")}'

        #авто заполнение товара
        for k in range(0, len(tovar)):
            for i in range(0, len(tovar[k])):
                self.root.ids[f"{tovar_content[k]}"].add_widget(
                    ContentTovar(naz = f"{tovar[k][i][0]}", cena = f"{tovar[k][i][3]}", tvod=f"{tovar[k][i][1]}", ind = k))

        #создание данных в вкладке поставщики
        self.on_start_postavshik()

        #время запуска приложения
        self.dialog = MDDialog(text = f"Время запуска: {datetime.today() - start_time}",)
        self.dialog.open()

################################################################################
#                   авто подсчёт товара                                        #
################################################################################
    def calc_tovar(self, values):
        itogo[values] = 0
        
        for i in range(0, len(tovar[values])):
            
            self.root.ids[tovar_content[values]].children[i].ids.tovar_field.text = self.root.ids[tovar_content[values]].children[i].ids.tovar_field.text.replace(',', '.')

            if self.root.ids[tovar_content[values]].children[i].ids.tovar_field.text == '':
                self.root.ids[tovar_content[values]].children[i].ids.tovar_field.text = '0'
                self.dialog = MDDialog(title = "ИСПРАВЛЕНО:", text = "было не заполнено количество товара, обнулино", radius=[20, 20, 20, 20], type='custom')
                self.dialog.open()
            elif len(self.root.ids[tovar_content[values]].children[i].ids.tovar_field.text)>1 and self.root.ids[tovar_content[values]].children[i].ids.tovar_field.text[0]=="0" and self.root.ids[tovar_content[values]].children[i].ids.tovar_field.text[1]!=".":
                self.root.ids[tovar_content[values]].children[i].ids.tovar_field.text = self.root.ids[tovar_content[values]].children[i].ids.tovar_field.text[1:]
                self.dialog = MDDialog(title = "ИСПРАВЛЕНО:", text = "первым символом был 0, обрезали", radius=[20, 20, 20, 20], type='custom')
                self.dialog.open()
            elif self.root.ids[tovar_content[values]].children[i].ids.tovar_cena.text == '':
                self.root.ids[tovar_content[values]].children[i].ids.tovar_cena.text = '0'
                self.dialog = MDDialog(title = "ИСПРАВЛЕНО:", text = "была не заполнена цена товара, обнулино", radius=[20, 20, 20, 20], type='custom')
                self.dialog.open()
        
        for i in range(0, len(tovar[values])):
            tovar[values][i][1] = self.root.ids[tovar_content[values]].children[i].ids.tovar_field.text
            tovar[values][i][2] = float(round(eval(tovar[values][i][1]), 3))
            tovar[values][i][3] = self.root.ids[tovar_content[values]].children[i].ids.tovar_cena.text
            tovar[values][i][4] = float(round((tovar[values][i][2]*float(tovar[values][i][3])), 3))
            self.root.ids[tovar_content[values]].children[i].ids.tovar_sum.text = f'{tovar[values][i][4]} грн'
            itogo[values] += tovar[values][i][4]

                
            if values==0:
                self.root.ids[tovar_content[values]].children[i].ids.tovar_col.text = f'{vodka[i][2]} л. по '
                self.root.ids.itogo_vodka.text = f'{itogo[0]}грн.'
                self.root.ids.vodka_summa.text = f'{itogo[0]}грн.'
            elif values==1:
                self.root.ids[tovar_content[values]].children[i].ids.tovar_col.text = f'{cognac[i][2]} л. по '
                self.root.ids.itogo_cognac.text = f'{itogo[1]}грн.'
                self.root.ids.cognac_summa.text = f'{itogo[1]}грн.'
            elif values==2:
                self.root.ids[tovar_content[values]].children[i].ids.tovar_col.text = f'{liquor[i][2]} л. по '
                self.root.ids.itogo_liquor.text = f'{itogo[2]}грн.'
                self.root.ids.liquor_summa.text = f'{itogo[2]}грн.'
            elif values==3:
                self.root.ids[tovar_content[values]].children[i].ids.tovar_col.text = f'{int(low_alcohol[i][2])} шт. по '
                self.root.ids.itogo_low_alcohol.text = f'{itogo[3]}грн.'
                self.root.ids.low_alcohol_summa.text = f'{itogo[3]}грн.'
            elif values==4:
                self.root.ids[tovar_content[values]].children[i].ids.tovar_col.text = f'{wine[i][2]} л. по '
                self.root.ids.itogo_wine.text = f'{itogo[4]}грн.'
                self.root.ids.wine_summa.text = f'{itogo[4]}грн.'
            elif values==5:
                for i in range(len(beer)-3, len(beer)):
                    self.root.ids[tovar_content[values]].children[i].ids.tovar_col.text = f'{beer[i][2]} л. по '
                for i in range(0, len(beer)-3):
                    self.root.ids[tovar_content[values]].children[i].ids.tovar_col.text = f'{int(beer[i][2])} шт. по '
                self.root.ids.itogo_beer.text = f'{itogo[5]}грн.'
                self.root.ids.beer_summa.text = f'{itogo[5]}грн.'
            elif values==6:
                self.root.ids[tovar_content[values]].children[i].ids.tovar_col.text = f'{int(k_beer[i][2])} шт. по '
                self.root.ids.itogo_k_beer.text = f'{itogo[6]}грн.'
                self.root.ids.k_beer_summa.text = f'{itogo[6]}грн.'
            elif values==7:
                for i in range(len(water)-8, len(water)):
                    self.root.ids[tovar_content[values]].children[i].ids.tovar_col.text = f'{int(water[i][2])} шт. по '
                for i in range(0, len(water)-8):
                    self.root.ids[tovar_content[values]].children[i].ids.tovar_col.text = f'{water[i][2]} л. по '
                self.root.ids.itogo_water.text = f'{itogo[7]}грн.'
                self.root.ids.water_summa.text = f'{itogo[7]}грн.'
            elif values==8:
                self.root.ids[tovar_content[values]].children[i].ids.tovar_col.text = f'{int(coffee[i][2])} г. по '
                self.root.ids.itogo_coffee.text = f'{itogo[8]}грн.'
                self.root.ids.coffee_summa.text = f'{itogo[8]}грн.'
            elif values==9:
                for i in range(len(other)-3, len(other)):
                    self.root.ids[tovar_content[values]].children[i].ids.tovar_col.text = f'{other[i][2]}л. по '
                for i in range(0, len(other)-3):
                    self.root.ids[tovar_content[values]].children[i].ids.tovar_col.text = f'{int(other[i][2])} шт. по '
                self.root.ids.itogo_other.text = f'{itogo[9]}грн.'
                self.root.ids.other_summa.text = f'{itogo[9]}грн.'

################################################################################
#                   подсчёт итоговой суммы                                     #
################################################################################
    def calc_itogo(self):
        self.root.ids.itogo_summa.text = f'{sum(itogo)}грн.'

################################################################################
#                   вставка данных в world файл по шаблону                     #
################################################################################
    def on_menu_right(self):

        tovar_docx = ['vod', 'cog', 'liq', 'low', 'wine', 'beer', 'k_beer', 'wat', 'cof', 'oth']

        context = {
            'title': f'{self.screen.ids.barmen.text}',
            'data': f'{self.screen.ids.start_date.text}',
            'ito_sum': f'{sum(itogo)}'}

        for k in range(len(tovar_docx)):
            context[f"sum_{tovar_docx[k]}"] = f'{itogo[k]}'
            for i in range(len(tovar[k])):
                context[f"{tovar_docx[k]}_naz{i}"] = tovar[k][i][0]
                context[f"{tovar_docx[k]}{i}"] = tovar[k][i][1]
                context[f"{tovar_docx[k]}_col{i}"] = tovar[k][i][2]
                context[f"{tovar_docx[k]}_cena{i}"] = tovar[k][i][3]
                context[f"{tovar_docx[k]}_sum{i}"] = tovar[k][i][4]
    
        mydoc = DocxTemplate("shablon.docx")
        mydoc.render(context)
        mydoc.save(f"doc{self.screen.ids.start_date.text}.docx")
        
        self.dialog = MDDialog(title = "ВЫПОЛНЕНО:", text = f"файл doc{self.screen.ids.start_date.text}.docx сохранен", radius=[20, 20, 20, 20], type='custom')
        self.dialog.open()

################################################################################
# изминение цен в базе данных по категориям                                    #
################################################################################
    def price_update_query(self, price_list, par):
        try:
            conn = sqlite3.connect('tovar.db')
            cur = conn.cursor()
            print("Подключен к SQLite для смены цен")
            
            if par==0:
                sqlite_update_query = """Update vodka set cena = ? where id = ?"""
            elif par==1:
                sqlite_update_query = """Update cognac set cena = ? where id = ?"""
            elif par==2:
                sqlite_update_query = """Update liquor set cena = ? where id = ?"""
            elif par==3:
                sqlite_update_query = """Update low_alcohol set cena = ? where id = ?"""
            elif par==4:
                sqlite_update_query = """Update wine set cena = ? where id = ?"""
            elif par==5:
                sqlite_update_query = """Update beer set cena = ? where id = ?"""
            elif par==6:
                sqlite_update_query = """Update k_beer set cena = ? where id = ?"""
            elif par==7:
                sqlite_update_query = """Update water set cena = ? where id = ?"""
            elif par==8:
                sqlite_update_query = """Update coffee set cena = ? where id = ?"""
            elif par==9:
                sqlite_update_query = """Update other set cena = ? where id = ?"""
            cur.executemany(sqlite_update_query, price_list)
            conn.commit()
            print("Записей", cur.rowcount, ". Успешно обновлены")
            self.dialog = MDDialog(title = "ВЫПОЛНЕНО:", text = "в этом разделе цены успешно обновлены", radius=[20, 20, 20, 20], type='custom')
                
            self.dialog.open()
            cur.close()
            
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)
            self.dialog = MDDialog(title = "ОШИБКА:", text = "проблема в работе с базой данных",)
            self.dialog.open()
        finally:
            if conn:
                conn.close()
                print("Соединение с SQLite закрыто")
            
    def price_update(self, par):
    
        price_list = []
        for i in range(0, len(tovar[par])):
            price_list.append((self.root.ids[tovar_content[par]].children[i].ids.tovar_cena.text, len(tovar[par])-i-1))
        
        self.price_update_query(price_list, par)

################################################################################
# изминение количества товара по умолчанию в базе данных                       #
################################################################################
    def col_vo_update_query(self, col_vo_list, par):
        try:
            conn = sqlite3.connect('tovar.db')
            cur = conn.cursor()
            print("Подключен к SQLite для смены цен")
            
            if par==0:
                sqlite_update_query = """Update vodka set stroka = ? where id = ?"""
            elif par==1:
                sqlite_update_query = """Update cognac set stroka = ? where id = ?"""
            elif par==2:
                sqlite_update_query = """Update liquor set stroka = ? where id = ?"""
            elif par==3:
                sqlite_update_query = """Update low_alcohol set stroka = ? where id = ?"""
            elif par==4:
                sqlite_update_query = """Update wine set stroka = ? where id = ?"""
            elif par==5:
                sqlite_update_query = """Update beer set stroka = ? where id = ?"""
            elif par==6:
                sqlite_update_query = """Update k_beer set stroka = ? where id = ?"""
            elif par==7:
                sqlite_update_query = """Update water set stroka = ? where id = ?"""
            elif par==8:
                sqlite_update_query = """Update coffee set stroka = ? where id = ?"""
            elif par==9:
                sqlite_update_query = """Update other set stroka = ? where id = ?"""
            cur.executemany(sqlite_update_query, col_vo_list)
            conn.commit()
            print("Записей", cur.rowcount, ". Успешно обновлены")
            self.dialog = MDDialog(title = "ВЫПОЛНЕНО:", text = "в этом разделе количество по умолчанию успешно обновлено", radius=[20, 20, 20, 20], type='custom')
                
            self.dialog.open()
            cur.close()
            
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)
            self.dialog = MDDialog(title = "ОШИБКА:", text = "проблема в работе с базой данных",)
            self.dialog.open()
        finally:
            if conn:
                conn.close()
                print("Соединение с SQLite закрыто")
            
    def col_vo_update(self, par):
    
        col_vo_list = []
        for i in range(0, len(tovar[par])):
            col_vo_list.append((self.root.ids[tovar_content[par]].children[i].ids.tovar_field.text, len(tovar[par])-i-1))
        
        self.col_vo_update_query(col_vo_list, par)

################################################################################
#                   ПОДСЧЁТ КУПЮР                                              #
################################################################################
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

################################################################################
#                   ПОСТАВЩИКИ                                                 #
################################################################################
    # создание данных в вкладке поставщики
    def on_start_postavshik(self):
        
        self.root.ids.con_post.clear_widgets()

        for i in range(0, len(contacti)):
            self.root.ids.con_post.add_widget(
                Content_Postavka(
                    cont_org = contacti[i][1],
                    cont_name = contacti[i][2],
                    cont_phone1 = contacti[i][3],
                    cont_ind = f'{i}'))

    # добавление контакта
    def new_postavshik(self):
        # перебираем id
        cont_list_id = []
        for i in range(0, len(contacti)):
            cont_list_id.append(contacti[i][0])
        # добавляем новый id
        if len(cont_list_id) == 0: cont_id = 1000
        else: cont_id = max(cont_list_id)+1

        contacti.append([
            cont_id,
            self.root.ids.post_org.text,
            self.root.ids.post_account.text,
            self.root.ids.post_number_phone1.text,
            self.root.ids.post_number_phone2.text,
            self.root.ids.post_note.text,])

        cont = (
            cont_id,
            self.root.ids.post_org.text,
            self.root.ids.post_account.text,
            self.root.ids.post_number_phone1.text,
            self.root.ids.post_number_phone2.text,
            self.root.ids.post_note.text,)

        try:
            conn = sqlite3.connect('tovar.db')
            cur = conn.cursor()
            print("Подключен к SQLite")

            sqlite_insert_query = """INSERT INTO contacti
                                (id, org, name, number1, number2, note)
                                VALUES (?, ?, ?, ?, ?, ?);"""
            cur.execute(sqlite_insert_query, cont)
            conn.commit()
            print("Запись успешно вставлена ​​в таблицу postavka ", cur.rowcount)
            cur.close()

        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)
        finally:
            if conn:
                conn.close()
                print("Соединение с SQLite закрыто")

        self.on_start_postavshik()

    # обнуление формы
    def new_post_clean(self):
        self.root.ids.post_org.text = ''
        self.root.ids.post_account.text = ''
        self.root.ids.post_number_phone1.text = ''
        self.root.ids.post_number_phone2.text = ''
        self.root.ids.post_note.text = ''
        self.root.ids.post_del.disabled = True
        self.root.ids.post_edit.disabled = True
        self.root.ids.post_new.disabled = False
        self.root.ids.screen_manager_post.current = "postav_input"

    # добавление данных для изминения контакта
    def upgrade_cont(self, number_cont):
        global del_postavshik
        del_postavshik = int(number_cont)
        self.root.ids.post_org.text = contacti[del_postavshik][1]
        self.root.ids.post_account.text = contacti[del_postavshik][2]
        self.root.ids.post_number_phone1.text = contacti[del_postavshik][3]
        self.root.ids.post_number_phone2.text = contacti[del_postavshik][4]
        self.root.ids.post_note.text = contacti[del_postavshik][5]
        self.root.ids.post_del.disabled = False
        self.root.ids.post_edit.disabled = False
        self.root.ids.post_new.disabled = True
        self.root.ids.screen_manager_post.current = "postav_input"

    # изминение контакта
    def upgrade_postavshik(self):
        
        contacti[del_postavshik] = [
            contacti[del_postavshik][0],
            self.root.ids.post_org.text,
            self.root.ids.post_account.text,
            self.root.ids.post_number_phone1.text,
            self.root.ids.post_number_phone2.text,
            self.root.ids.post_note.text,]

        cont = (
            self.root.ids.post_org.text,
            self.root.ids.post_account.text,
            self.root.ids.post_number_phone1.text,
            self.root.ids.post_number_phone2.text,
            self.root.ids.post_note.text,
            contacti[del_postavshik][0])

        try:
            conn = sqlite3.connect('tovar.db')
            cur = conn.cursor()
            print("Подключен к SQLite")

            sqlite_insert_query = """Update contacti set org = ?, name = ?, number1 = ?, number2 = ?, note = ? where id = ?"""
            cur.execute(sqlite_insert_query, cont)
            conn.commit()
            print("Запись успешно обновлена ​​в таблицу postavka ", cur.rowcount)
            cur.close()

        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)
        finally:
            if conn:
                conn.close()
                print("Соединение с SQLite закрыто")

        self.on_start_postavshik()

    # удаление контакта
    def delete_postavshik(self):
        dev_id = contacti[del_postavshik][0]
        contacti.pop(del_postavshik)

        try:
            conn = sqlite3.connect('tovar.db')
            cur = conn.cursor()
            print("Подключен к SQLite")

            sqlite_insert_query = """DELETE from contacti where id = ?"""
            cur.execute(sqlite_insert_query, (dev_id, ))
            conn.commit()
            print("Запись успешно удалена")
            cur.close()

        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)
        finally:
            if conn:
                conn.close()
                print("Соединение с SQLite закрыто")
        
        self.on_start_postavshik()

################################################################################
#                   ВКЛАДКА О МОРЕ!!!                                          #
################################################################################
    def omore_random(self):
        more_id = random.randint(0, 100)
        self.omore(more_id)

    def omore(self, more_id):
        try:
            conn = sqlite3.connect('tovar.db')
            cur = conn.cursor()
            print("База данных создана и успешно подключена к SQLite")

            sql_select = """SELECT * from omore where id = ?"""
            cur.execute(sql_select, (more_id,))
            records = cur.fetchall()
            for row in records:
                self.root.ids.lab_more.text = row[1]

            cur.close()
    
        except sqlite3.Error as error:
            print("Ошибка при подключении к sqlite", error)
        finally:
            if (conn):
                conn.close()
                print("Соединение с SQLite закрыто")


KanaKy().run()