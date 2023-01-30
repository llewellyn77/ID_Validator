import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# Load the data from the excel file
df = pd.read_excel("ID_Validator.xlsx")

# Create a webdriver instance
driver = webdriver.Chrome(executable_path=r"C:\Users\Llewellyn\Documents\ID_Validator\Chrome_driver\chromedriver.exe")
# Enables Logging
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)

# Navigate to the website
driver.get("https://www.checkid.co.za/")

# Iterate through the "ID" column in the excel file
for id_value in df["ID"]:
    # Locate the input field and enter the ID value
    input_field = driver.find_element(By.ID,"searchBox")
    input_field.clear()
    input_field.send_keys(id_value)
    input_field.send_keys(Keys.RETURN)

    # Wait for the result to load
    time.sleep(3)

    # Extract the result elements
    result_box = driver.find_element(By.XPATH,'/html/body/main/div/div/div[3]/div[1]/div/div[3]').text
    print(result_box)
    # String manipulation of each result
    is_valid = result_box.splitlines()[0]
    is_valid_cleaned = is_valid[2:].strip()
    born = result_box.splitlines()[1].split(': ')[1]
    age = result_box.splitlines()[2].split(': ')[1]
    gender = result_box.splitlines()[3].split(': ')[1]
    citizenship = result_box.splitlines()[4].split(': ')[1]  
   
    #Update the data in the excel file
    df.loc[df["ID"] == id_value, "Is Valid"] = is_valid_cleaned
    df.loc[df["ID"] == id_value, "Born"] = born
    df.loc[df["ID"] == id_value, "Age"] = age
    df.loc[df["ID"] == id_value, "Gender"] = gender
    df.loc[df["ID"] == id_value, "Citizenship"] = citizenship

    print(df)

# Save the updated data to the excel file
df.to_excel("ID_Validator.xlsx", index=False)

# Close the webdriver instance
#driver.quit()
