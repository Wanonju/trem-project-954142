from datetime import date, timedelta 

#ชื่อ, หน่วย, คงเหลือ, ขั้นต่ำ, วันหมดอายุ
today = date.today()
stock = [
    ["ขนมปังแผ่น",     "แผ่น", 100, 20, today + timedelta(days=7)],
    ["วิปครีม",         "กรัม", 2000, 500, today + timedelta(days=4)],
    ["ไข่หวาน",        "กรัม", 800, 200, today + timedelta(days=4)],
    ["ช็อกโกแลตซอส",   "กรัม", 600, 150, today + timedelta(days=60)],
    ["สตรอว์เบอร์รี",   "กรัม", 500, 150, today + timedelta(days=3)],
]

#ชื่อเมนู, ราคา, ลำดับของไส้ใน stock
menu = [
    ["แซนวิชวิปครีมไข่หวาน", 25, 2],
    ["แซนวิชวิปครีมช็อกโกแลต", 25, 3],
    ["แซนวิชวิปครีมสตรอว์เบอร์รี", 30, 4],
]


sold = [0, 0, 0]


BREAD_USE = 2      
CREAM_USE = 50     
FILLING_USE = 30   


def get_number(message, low, high):
    while True:
        text = input(message)
        if text.isdigit():
            number = int(text)
            if number >= low and number <= high:
                return number
        print("กรอกผิด ต้องเป็นตัวเลข", low, "ถึง", high)


def show_stock(stock):
    print("\n--- สต๊อกวัตถุดิบ ---")
    for i in range(len(stock)):
        row = stock[i]
        print(i + 1, ".", row[0], "คงเหลือ", row[2], row[1],
              "(ขั้นต่ำ", row[3], ")")


def add_stock(stock, index, qty):
    stock[index][2] += qty
    return stock[index][2]


def can_sell(stock, filling_index, qty):
    need_bread = BREAD_USE * qty
    need_cream = CREAM_USE * qty
    need_filling = FILLING_USE * qty
    if stock[0][2] >= need_bread and stock[1][2] >= need_cream and stock[filling_index][2] >= need_filling:
        return True
    return False


def sell_sandwich(stock, menu, sold, menu_index, qty):
    filling_index = menu[menu_index][2]
    if can_sell(stock, filling_index, qty) == False:
        return 0
    stock[0][2] = stock[0][2] - BREAD_USE * qty
    stock[1][2] = stock[1][2] - CREAM_USE * qty
    stock[filling_index][2] = stock[filling_index][2] - FILLING_USE * qty
    sold[menu_index] = sold[menu_index] + qty
    return menu[menu_index][1] * qty


def find_low_stock(stock):
    low_list = []
    for row in stock:
        if row[2] <= row[3]:
            low_list.append(row[0])
    return low_list


def find_expiring(stock, days):
    result = []
    for row in stock:
        days_left = (row[4] - date.today()).days
        if days_left <= days and row[2] > 0:
            result.append([row[0], days_left])
    return result


def show_summary(menu, sold):
    print("\n--- สรุปยอดขายวันนี้ ---")
    total = 0
    best_index = 0
    for i in range(len(menu)):
        money = menu[i][1] * sold[i]
        total = total + money
        print(menu[i][0], ":", sold[i], "ชิ้น =", money, "บาท")
        if sold[i] > sold[best_index]:
            best_index = i
    print("รายได้รวม:", total, "บาท")
    if total > 0:
        print("เมนูขายดีที่สุด:", menu[best_index][0])
    else:
        print("วันนี้ยังไม่มีการขาย")
    return total

def show_main_menu():
    print("\n===== ระบบสต๊อกร้านแซนวิชวิปครีมผมไม้ =====")
    print("1. ดูสต๊อก")
    print("2. รับของเข้า")
    print("3. ขายแซนวิช")
    print("4. เช็คของใกล้หมด")
    print("5. เช็คของใกล้หมดอายุ")
    print("6. สรุปยอดขาย")
    print("7. ออกจากโปรแกรม")


running = True
while running:
    show_main_menu()
    choice = get_number("เลือกเมนู (1-7): ", 1, 7)

    if choice == 1:
        show_stock(stock)

    elif choice == 2:
        show_stock(stock)
        item = get_number("เลือกลำดับวัตถุดิบ: ", 1, len(stock))
        qty = get_number("จำนวนที่รับเข้า: ", 1, 10000)
        new_qty = add_stock(stock, item - 1, qty)
        print("รับเข้าแล้ว ตอนนี้", stock[item - 1][0], "มี", new_qty,
              stock[item - 1][1])

    elif choice == 3:
        print("\n--- เมนูแซนวิช ---")
        for i in range(len(menu)):
            print(i + 1, ".", menu[i][0], "ราคา", menu[i][1], "บาท")
        m = get_number("เลือกเมนู: ", 1, len(menu))
        qty = get_number("จำนวนที่ขาย: ", 1, 100)
        money = sell_sandwich(stock, menu, sold, m - 1, qty)
        if money > 0:
            print("ขายสำเร็จ ได้เงิน", money, "บาท")
            low_list = find_low_stock(stock)
            if len(low_list) > 0:
                print("เตือน! ของใกล้หมด:", low_list)
        else:
            print("ขายไม่ได้ วัตถุดิบไม่พอ")

    elif choice == 4:
        low_list = find_low_stock(stock)
        print("\n--- ของใกล้หมด ---")
        if len(low_list) == 0:
            print("ยังไม่มีของใกล้หมด")
        for name in low_list:
            print("-", name)

    elif choice == 5:
        days = get_number("เตือนล่วงหน้ากี่วัน (0-30): ", 0, 30)
        expiring = find_expiring(stock, days)
        print("\n--- ของใกล้หมดอายุ ---")
        if len(expiring) == 0:
            print("ไม่มีของใกล้หมดอายุ")
        for name, days_left in expiring:
            if days_left < 0:
                print("-", name, "หมดอายุแล้ว! ห้ามใช้")
            elif days_left == 0:
                print("-", name, "หมดอายุวันนี้")
            else:
                print("-", name, "เหลืออีก", days_left, "วัน")

    elif choice == 6:
        show_summary(menu, sold)

    else:
        print("ขอบคุณที่ใช้งาน")
        running = False