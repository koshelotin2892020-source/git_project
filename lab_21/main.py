import requests
import matplotlib.pyplot as plt

base_url = 'https://pokeapi.co/api/v2/'
limit = 10
url = f'{base_url}pokemon?limit={limit}'

data = []

r = requests.get(url).json()
for i in r['results']:
    s = requests.get(i['url']).json()
    data.append({
        'id': s['id'],
        'name': s['forms'][0]['name'],
        'height': s['height'],
        'weight': s['weight'],
        'hp': s['stats'][0]['base_stat'],
        'attack': s['stats'][1]['base_stat'],
        'defense': s['stats'][2]['base_stat'],
        'speed': s['stats'][5]['base_stat'],
    })
    # print(s['height']) # рост
    # print(s['weight']) # вес
    # print(s['forms'][0]['name']) # имя покемона
    # print(s['id']) # id покемонов
    # print(s['stats']) # статы покемонов

print(data)
plt.plot([x['id'] for x in data], [x['speed'] for x in data])
plt.xlabel('id покемона')
plt.ylabel('Скорость покемона')
plt.title('График зависимости скорости от id покемона')
plt.show()

plt.scatter([x['hp'] for x in data], [x['attack'] for x in data])
plt.xlabel('Здоровье покемона')
plt.ylabel('Атака покемона')
plt.title('Разброс точек hp/attack покемонов')
plt.show()

plt.bar([x['name'] for x in data], [x['hp'] for x in data])
plt.xlabel('Имя покемона')
plt.ylabel('Здоровье покемона')
plt.title('Столбчатая диаграмма здоровья покемонов')
plt.show()

plt.barh([x['name'] for x in data], [x['defense'] for x in data])
plt.xlabel('Защита покемона')
plt.title('Горизонтальная столбчатая диаграмма защиты покемонов')
plt.show()

plt.hist([x['height'] for x in data], width=0.1)
plt.xlabel('Рост покемона')
plt.title('Гистограмма роста покемонов')
plt.show()

plt.pie([x['hp'] for x in data], labels=[x['name'] for x in data], autopct='%1.1f%%')
plt.xlabel('Здоровье покемона')
plt.title('Круговая диаграмма здоровья покемонов')
plt.show()

plt.boxplot([x['attack'] for x in data])
plt.ylabel('Разброс урона покемона')
plt.title('Boxplot')
plt.show()
