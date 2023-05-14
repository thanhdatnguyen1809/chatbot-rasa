import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
# Make a request to the websites
page_index =1
count =0
check =True
data =[]
while check:
        url = f"https://philong.com.vn/tim?scat_id=&q=&page={page_index}"
        response = requests.get(url)
        

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        # Find all product categories
        products = soup.find_all('div', class_='p-item')
        website = "https://philong.com.vn"
        if products ==[]:
            break
        page_index+=1
        # Loop through each category and extract relevant information
        for product in products:
            # Extract the category name
            
            try:

                name = product.find('h4').text.strip()
                price = product.find(class_='p-price').text.strip()
                unprice = product.find(class_='p-unprice').text.strip()
                # if unprice == "":
                #      unprice ="0"
                # print(unprice)
                # unprice ="test"
                # sale = product.find(class_ ='p-sale').text.strip() 
                # promotion = product.find(class_ ='p-promotion').text.strip() 
                summary = product.find(class_='p-summary').text.strip()
                status=1
                if (product.find(class_='btn-add')!=None):
                    status =1
                else:
                    status =0

                if (product.find(class_='p-sale')!=None):
                    sale = product.find(class_ ='p-sale').text.strip() 
                else:
                    sale ="N/A"
                if (product.find(class_='p-promotion')!=None):
                    promotion = product.find(class_ ='p-promotion').text.strip() 
                else:
                    promotion ="N/A"
                row = [website,name,price,unprice,sale,promotion,summary,status,]
                
                data.append(row)
            except AttributeError:
                sale =''
                promotion=''
                unprice =0
            
       

print(len(data))
df = pd.DataFrame(data, columns=['Website','Name', 'Price', 'Unprice','Sale','Promotion','Summary','Status'])
df.to_csv('crawl.csv', index=False)
