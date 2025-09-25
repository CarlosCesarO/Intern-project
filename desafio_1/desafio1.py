import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('./CarsData.csv')

df = df[df['year'] >= 2010] 

economicos = df.groupby('Manufacturer')['mpg'].mean().sort_values(ascending=False).head(10)

plt.figure(figsize=(5,3))
economicos.plot(kind='bar', color='blue')
plt.title('Marcas mais econômicos')
plt.xlabel('Fabricante')
plt.ylabel('MPG')
plt.show()

print("")

df = df[df['Manufacturer'] == "toyota"] 
toyota = df.groupby('model')['price'].mean().sort_values(ascending=True).head(10)

plt.figure(figsize=(5,3))
toyota.plot(kind='bar', color='green')
plt.title('Mais baratos Toyota')
plt.xlabel('Modelo')
plt.ylabel('Preço $')
plt.show()