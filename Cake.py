import datetime
from fpdf import FPDF
import requests
#ordering a cake program

def main():
    size = quantity()
    flavours = flavour()
    baketime, invoicedue = date()
    egg_price = eggprice(size, flavours)

    invoice(size, flavours, baketime, invoicedue, egg_price)


#find out the amount of people eating the cake
def quantity():
    try:
        people = int(input("How many people will eat this cake?:"))
        if people <= 0:
            raise ValueError
        elif people < 10:
            size = "6inch cake"
        elif people < 30:
            size = "8inch cake"
        elif people < 50:
            size = "10inch cake"
        else:
            n = round(people, -1)//10
            size = f"{n} sheet cakes"
        return size
    except ValueError:
        print("Please input a positive whole number")


#find out what flavours they want
def flavour():
    flavours = {"sponge":"", "icing":"", "filling":""}
    while True:
        try:
            sponge = input("Do you want vanilla or chocolate sponge?").lower()
            if sponge in ["chocolate", "vanilla"]:
                flavours["sponge"] = sponge
                break
            else:
                raise ValueError

        except ValueError:
            print("please input chocolate or vanilla")
    while True:
        try:
            icing = input("Do you want pink, blue, green or chocolate icing?").lower()
            if icing not in ["pink", "blue", "green", "chocolate"]:
                raise ValueError
            else:
                flavours["icing"] = icing
                break
        except ValueError:
            print("Please input pink, blue, green or chocolate")
    while True:
        try:
            filling = input("Do you want custard or jam filling?").lower()
            if filling not in ["custard", "jam"]:
                raise ValueError
            else:
                flavours["filling"] = filling
                break
        except ValueError:
            print("Please input custard or jam")

    return flavours

#find out date and time of event

def date():
    today = datetime.date.today()

    year = int(input("Year of event:"))
    month = int(input("Month of event:"))
    day = int(input("Day of event:"))
    eventdate = datetime.date(year, month, day)

    baketime = eventdate - today
    invoicedue = eventdate + datetime.timedelta(days=30)

    return baketime, invoicedue

def invoice(size, flavours, baketime, invoicedue, egg_price):

    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Times", size=20)
    pdf.cell(0, 10, "Cake Order", new_x = "LMARGIN", new_y = "NEXT", align= "C")

    pdf.cell(0, 10, f"size = {size}", new_x = "LMARGIN", new_y = "NEXT", align= "L" )
    pdf.cell(0, 10, f"size = {flavours['sponge']}", new_x = "LMARGIN", new_y = "NEXT", align= "L" )
    pdf.cell(0, 10, f"size = {flavours['icing']}", new_x = "LMARGIN", new_y = "NEXT", align= "L" )
    pdf.cell(0, 10, f"size = {flavours['filling']}", new_x = "LMARGIN", new_y = "NEXT", align= "L" )

    pdf.cell(0, 10, f"Price = £{egg_price:.2f} new_x = "LMARGIN", new_y = "NEXT", align= "C")
    pdf.cell(0, 10, f"Invoice Due: {invoicedue}", new_x = "LMARGIN", new_y = "NEXT", align= "C")

    pdf.output("cake_order.pdf")

if __name__ in "__main__":
    main()

# Vanilla 6inch cake needs 3 eggs find the price of eggs based on the market and add it to the price of the cake.
#Dictionary of how many eggs in each cake
Ingredients_eggs = {"vanilla 6inch": 3, "chocolate 6inch": 4, "vanilla 8inch": 4, "chocolate 8inch": 7, "vanilla 10inch": 5, "chocolate 10inch": 9, "vanilla sheetcake": 12, "chocolate sheetcake": 14}

# calculate the price of eggs you need for the cake
def eggprice():
    if size == "6inch cake" and flavours["sponge"] == "vanilla":
        eggs = 3
    else:
        eggs = 0

    eggpack_price == 1.80
    pack_size == 6

    price_per_egg == (eggpack_price/pack_size)
    total = eggs * price_per_egg

    return total

#Use an API to get an up to date price of eggpack
def get_egg_price():
    response = request.get( "https://prices.openfoodfacts.org/api/v1/prices", params =
                           {"product_code": "YOUR_EGG_PACK_BARCODE","currency": "GBP","order_by": "-date","size": 1,}
                           timeout = 10)
    response.raise_for_status()
    data = response.json()
    return eggpack_price = data["price"]

