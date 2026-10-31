import datetime
from fpdf import FPDF
import requests
import csv
import matplotlib.pyplot as plt
import datetime
#ordering a cake program

def main():
    size = quantity()
    flavours = flavour()
    baketime, invoicedue = date()

    eggpack_price = get_egg_price()
    egg_price = eggprice(size, flavours, eggpack_price)

    save_price(eggpack_price)
    plot_prices()

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
    pdf.cell(0, 10, f"Sponge: {flavours['sponge']}", new_x="LMARGIN", new_y="NEXT", align="L")
    pdf.cell(0, 10, f"Icing: {flavours['icing']}", new_x="LMARGIN", new_y="NEXT", align="L")
    pdf.cell(0, 10, f"Filling: {flavours['filling']}", new_x="LMARGIN", new_y="NEXT", align="L")

    pdf.cell(0, 10, f"Egg Price = £{egg_price:.2f}", new_x = "LMARGIN", new_y = "NEXT", align= "C")
    pdf.cell(0, 10, f"Invoice Due: {invoicedue}", new_x = "LMARGIN", new_y = "NEXT", align= "C")

    pdf.output("cake_order.pdf")

# Vanilla 6inch cake needs 3 eggs find the price of eggs based on the market and add it to the price of the cake.
#Dictionary of how many eggs in each cake
Ingredients_eggs = {"vanilla 6inch": 3, "chocolate 6inch": 4, "vanilla 8inch": 4, "chocolate 8inch": 7, "vanilla 10inch": 5, "chocolate 10inch": 9, "vanilla sheetcake": 12, "chocolate sheetcake": 14}

# calculate the price of eggs you need for the cake
def eggprice(size, flavours, eggpack_price):
    if "sheet cakes" in size:
        number_of_cakes = int(size.split()[0])
        cake_size = "sheetcake"
    else:
        number_of_cakes = 1
        cake_size = size.split()[0]

    key = f"{flavours['sponge']} {cake_size}"
    eggs = Ingredients_eggs[key] * number_of_cakes

    pack_size = 6

    price_per_egg = eggpack_price / pack_size
    return eggs * price_per_egg

#Use an API to get an up to date price of eggpack
def get_egg_price():
    response = requests.get("https://prices.openfoodfacts.org/api/v1/prices",
        params={
            "product_code": "5000306004240",
            "currency": "GBP",
            "order_by": "-date",
            "size": 1,},
        timeout=10,)

    response.raise_for_status()
    data = response.json()

    if not data["items"]:
        raise ValueError("No GBP price found for this egg pack")
    
    return float(data["items"][0]["price"])

#Save the price of eggs to a CSV file with the date
def save_price(egg_price):
    today = datetime.date.today().isoformat()

    with open("egg_prices.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([today, egg_price])

#open the csv, read it and organise the dates into one list and prices into another list and then plot them. 
def plot_prices():
    dates = []
    prices = []

    with open("egg_prices.csv", "r") as file:
        reader = csv.reader(file)

        for row in reader:
            dates.append(row[0])
            prices.append(float(row[1]))

    plt.plot(dates, prices, marker="o")
    plt.xlabel("Date")
    plt.ylabel("Egg Price (£)")
    plt.title("Egg Prices")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("egg_price_history.png")
    plt.close()

if __name__ == "__main__":
    main()