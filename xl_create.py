import xlsxwriter
from datetime import datetime

def writer(parametr):
    filename = f"Новости_{datetime.now().strftime('%Y_%m_%d_%H-%M-%S')}.xlsx"
    folder = input(fr"""Скопируйте путь до папки.
Например C:\Users\User\XLfiles
Ваш путь: """)
    try:
        book = xlsxwriter.Workbook(rf"{folder}\{filename}")
        page = book.add_worksheet(f"Новости")

        row = 0
        column = 0

        page.set_column("A:A",20)
        page.set_column("B:B",20)
        page.set_column("C:C",50)
        page.set_column("D:D", 50)

        for item in parametr:
            page.write(row, column, item[0])
            page.write(row, column+1, item[1])
            page.write(row, column+2, item[2])
            page.write(row, column + 3, item[3])
            row += 1

        book.close()
    except:
        print("Ошибка пути. ХL файл не создался.")
