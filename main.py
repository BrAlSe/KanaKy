from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ListProperty, ObjectProperty

from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior
from kivymd.uix.list import OneLineIconListItem, MDList

from kivymd.uix.tab import MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout

from kivymd.icon_definitions import md_icons
from kivymd.font_definitions import fonts

from kivymd.uix.picker import MDDatePicker

from kivymd.uix.dialog import MDDialog

from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp

from kivy.clock import Clock
from kivy.core.window import Window

import datetime
import sqlite3
from docxtpl import DocxTemplate

Window.softinput_mode = "below_target"

try:
    conn = sqlite3.connect('tovar.db')
    cur = conn.cursor()
    print("База данных создана и успешно подключена к SQLite")
    
    # Получите имя таблицы, сохраните его в списке table_name
    cur.execute("select name from sqlite_master where type='table'")
    table_name=cur.fetchall()
    table_name=[table_name[x][0] for x in range(len(table_name))]

    # tovar_dict = dict()

    cur.execute("SELECT * from vodka")
    records = cur.fetchall()
    vodka = []
    for row in records:
        vodka.append(list(row))
    
    # tovar_dict['vodka'] = vodka
            
    cur.execute("SELECT * from cognac")
    records = cur.fetchall()
    cognac = []
    for row in records:
        cognac.append(list(row))
           
    # tovar_dict['cognac'] = cognac
         
    cur.execute("SELECT * from liquor")
    records = cur.fetchall()
    liquor = []
    for row in records:
        liquor.append(list(row))
           
    # tovar_dict['liquor'] = liquor
         
    cur.execute("SELECT * from low_alcohol")
    records = cur.fetchall()
    low_alcohol = []
    for row in records:
        low_alcohol.append(list(row))
           
    # tovar_dict['low_alcohol'] = low_alcohol
         
    cur.execute("SELECT * from wine")
    records = cur.fetchall()
    wine = []
    for row in records:
        wine.append(list(row))
           
    # tovar_dict['wine'] = wine
         
    cur.execute("SELECT * from beer")
    records = cur.fetchall()
    beer = []
    for row in records:
        beer.append(list(row))
           
    # tovar_dict['beer'] = beer
         
    cur.execute("SELECT * from k_beer")
    records = cur.fetchall()
    k_beer = []
    for row in records:
        k_beer.append(list(row))
           
    # tovar_dict['k_beer'] = k_beer
         
    cur.execute("SELECT * from water")
    records = cur.fetchall()
    water = []
    for row in records:
        water.append(list(row))
           
    # tovar_dict['water'] = water
         
    cur.execute("SELECT * from coffee")
    records = cur.fetchall()
    coffee = []
    for row in records:
        coffee.append(list(row))
            
    # tovar_dict['coffee'] = coffee
         
    cur.execute("SELECT * from other")
    records = cur.fetchall()
    other = []
    for row in records:
        other.append(list(row))
          
    # tovar_dict['other'] = other
         
    cur.close()
    
except sqlite3.Error as error:
    print("Ошибка при подключении к sqlite", error)
finally:
    if (conn):
        conn.close()
        print("Соединение с SQLite закрыто")

    # print((tovar_dict[2])
    # for i in tovar_dict.keys():
        # print(i)
    
tovar = [vodka, cognac, liquor, low_alcohol, wine, beer, k_beer, water, coffee, other]
# tovar = ['vodka', 'cognac', 'liquor', 'low_alcohol', 'wine, beer', 'k_beer', 'water', 'coffee', 'other']
tovar_rus = ['Водка', 'Коньяк', 'Ликёр', 'Слабоалкоголка', 'Вино', 'Пиво', 'К Пиво', 'Вода', 'Кофе', 'Разное']

itogo = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
bills_nom = [1000, 500, 200, 100, 50, 20, 10, 5, 2, 1, 10, 5, 2, 1, 0.5, 0.1]
bills_col = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

class Tab(MDFloatLayout, MDTabsBase):
    pass

class ContentNavigationDrawer(MDBoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()

class ItemDrawer(OneLineIconListItem):
    icon = StringProperty()
    text_color = ListProperty((0, 0, 0, 1))

class DrawerList(ThemableBehavior, MDList):
    def set_color_item(self, instance_item):
        '''Called when tap on a menu item.'''

        # Установите цвет значка и текста для пункта меню.
        for item in self.children:
            if item.text_color == self.theme_cls.primary_color:
                item.text_color = self.theme_cls.text_color
                break
        instance_item.text_color = self.theme_cls.primary_color


class IconListItem(OneLineIconListItem):
    icon = StringProperty()
 
 
class KanaKy(MDApp):
    title = 'KanaKy'
    by_who = 'by BrAlSe  "ver: beta_1.0"'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_file('interface.kv')
        
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
            width_mult=4,
        )
        self.menu.bind()

    def set_item(self, text_item):
        self.screen.ids.barmen.text = text_item
        self.menu.dismiss()
         
    def build(self):
        return self.screen

    # функция даты on_save, on_cancel, date_dialog
    def on_save(self, instance, value, date_range):
        self.screen.ids.start_date.text = f"{value}"

    def on_cancel(self, instance, value):
        '''Events called when the "CANCEL" dialog box button is clicked.'''
        
    def date_dialog(self):
        date_dialog = MDDatePicker(min_year = 2021, max_year = 2030)
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()
    
    def on_start(self):
        
        self.screen.ids.start_date.text = f'{datetime.date.today()}'

        # присваиваем значение по умолчанию в MDTextField для ввода кол-ва + название
        for k in range(0, len(tovar)):
            for i in range(0, len(tovar[k])):
                self.screen.ids[tovar[k][i][2]].text = tovar[k][i][3]
                self.screen.ids[tovar[k][i][6]].text = tovar[k][i][7]
                self.screen.ids[tovar[k][i][0]].text = tovar[k][i][1]
        
        # for i in range(0, 16):
            # self.root.ids[f'bills{i}'].text = '0'
         
    # вставка данных в world файл по шаблону
    def on_menu_right(self):
        context = {
            'title': f'{self.screen.ids.barmen.text}',
            'data': f'{self.screen.ids.start_date.text}',
            'sum_vod': f'{itogo[0]}',
            'sum_cog': f'{itogo[1]}',
            'sum_liq': f'{itogo[2]}',
            'sum_low': f'{itogo[3]}',
            'sum_wine': f'{itogo[4]}',
            'sum_beer': f'{itogo[5]}',
            'sum_kb': f'{itogo[6]}',
            'sum_wat': f'{itogo[7]}',
            'sum_cof': f'{itogo[8]}',
            'sum_oth': f'{itogo[9]}',
            'ito_sum': f'{sum(itogo)}'}

        for k in range(0, len(tovar)):
            for i in range(0, len(tovar[k])):
                context[tovar[k][i][0]] = tovar[k][i][1]
                context[tovar[k][i][2]] = tovar[k][i][3]
                context[tovar[k][i][4]] = tovar[k][i][5]
                context[tovar[k][i][6]] = tovar[k][i][7]
                context[tovar[k][i][8]] = tovar[k][i][9]
                
        mydoc = DocxTemplate("shablon.docx")
        mydoc.render(context)
        mydoc.save(f"doc{self.screen.ids.start_date.text}.docx")
        
        self.dialog = MDDialog(title = "ВЫПОЛНЕНО:", text = f"файл doc{self.screen.ids.start_date.text}.docx сохранен", radius=[20, 20, 20, 20], type='custom')
        self.dialog.open()
        
        
        
    def calc_tovar(self, values):
        itogo[values] = 0
        
        for i in range(0, len(tovar[values])):
            if self.screen.ids[tovar[values][i][2]].text == '':
                self.screen.ids[tovar[values][i][2]].text = '0'
                self.dialog = MDDialog(title = "ОШИБКА:", text = "было не заполнено количество товара, обнулино",)
                self.dialog.open()
            elif self.screen.ids[tovar[values][i][6]].text == '':
                self.screen.ids[tovar[values][i][6]].text = '0'
                self.dialog = MDDialog(title = "ОШИБКА:", text = "была не заполнена цена товара, обнулино",)
                self.dialog.open()
        
        for i in range(0, len(tovar[values])):
            if self.screen.ids[tovar[values][i][2]].text.find(',') == -1:
                tovar[values][i][3] = self.screen.ids[tovar[values][i][2]].text
                tovar[values][i][5] = float(round(eval(tovar[values][i][3]), 3))
                tovar[values][i][7] = self.screen.ids[tovar[values][i][6]].text
                tovar[values][i][9] = float(round((tovar[values][i][5]*float(tovar[values][i][7])), 3))
                self.screen.ids[tovar[values][i][8]].text = f'{tovar[values][i][9]} грн'
                itogo[values] += tovar[values][i][9]
            else:
                self.screen.ids[tovar[values][i][2]].text = self.screen.ids[tovar[values][i][2]].text.split(',')[0]
                self.dialog = MDDialog(title = "ОШИБКА:", text = "нельзя использовать ЗАПЯТУЮ, только через ТОЧКУ", radius=[20, 20, 20, 20], type='custom')
                self.dialog.open()
                return
                
            if values==0:
                self.screen.ids[vodka[i][4]].text = f'{vodka[i][5]} л. по '
                self.root.ids.itogo_vodka.text = f'{itogo[0]}грн.'
                self.root.ids.vodka_summa.text = f'{itogo[0]}грн.'
            elif values==1:
                self.screen.ids[cognac[i][4]].text = f'{cognac[i][5]} л. по '
                self.root.ids.itogo_cognac.text = f'{itogo[1]}грн.'
                self.root.ids.cognac_summa.text = f'{itogo[1]}грн.'
            elif values==2:
                self.screen.ids[liquor[i][4]].text = f'{liquor[i][5]} л. по '
                self.root.ids.itogo_liquor.text = f'{itogo[2]}грн.'
                self.root.ids.liquor_summa.text = f'{itogo[2]}грн.'
            elif values==3:
                self.screen.ids[low_alcohol[i][4]].text = f'{int(low_alcohol[i][5])} шт. по '
                self.root.ids.itogo_low_alcohol.text = f'{itogo[3]}грн.'
                self.root.ids.low_alcohol_summa.text = f'{itogo[3]}грн.'
            elif values==4:
                self.screen.ids[wine[i][4]].text = f'{wine[i][5]} л. по '
                self.root.ids.itogo_wine.text = f'{itogo[4]}грн.'
                self.root.ids.wine_summa.text = f'{itogo[4]}грн.'
            elif values==5:
                for i in range(0, 3):
                    self.screen.ids[beer[i][4]].text = f'{beer[i][5]} л. по '
                for i in range(3, len(beer)):
                    self.screen.ids[beer[i][4]].text = f'{int(beer[i][5])} шт. по '
                self.root.ids.itogo_beer.text = f'{itogo[5]}грн.'
                self.root.ids.beer_summa.text = f'{itogo[5]}грн.'
            elif values==6:
                self.screen.ids[k_beer[i][4]].text = f'{int(k_beer[i][5])} шт. по '
                self.root.ids.itogo_k_beer.text = f'{itogo[6]}грн.'
                self.root.ids.k_beer_summa.text = f'{itogo[6]}грн.'
            elif values==7:
                for i in range(0, 8):
                    self.screen.ids[water[i][4]].text = f'{int(water[i][5])} шт. по '
                for i in range(8, len(water)):
                    self.screen.ids[water[i][4]].text = f'{water[i][5]} л. по '
                self.root.ids.itogo_water.text = f'{itogo[7]}грн.'
                self.root.ids.water_summa.text = f'{itogo[7]}грн.'
            elif values==8:
                self.screen.ids[coffee[i][4]].text = f'{int(coffee[i][5])} г. по '
                self.root.ids.itogo_coffee.text = f'{itogo[8]}грн.'
                self.root.ids.coffee_summa.text = f'{itogo[8]}грн.'
            elif values==9:
                for i in range(0, 3):
                    self.screen.ids[other[i][4]].text = f'{other[i][5]}л. по '
                for i in range(3, len(other)):
                    self.screen.ids[other[i][4]].text = f'{int(other[i][5])} шт. по '
                self.root.ids.itogo_other.text = f'{itogo[9]}грн.'
                self.root.ids.other_summa.text = f'{itogo[9]}грн.'
        
    def calc_itogo(self):
        self.root.ids.itogo_summa.text = f'{sum(itogo)}грн.'

    # изминение цен в базе данных по категориям
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
            price_list.append((self.screen.ids[tovar[par][i][6]].text, i))
        
        self.price_update_query(price_list, par)
        
    # подсчёт купюр
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
            self.root.ids[f'bills{i}'].text = '0'
        self.calc_bills()
                
KanaKy().run()
