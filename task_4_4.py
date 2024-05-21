# -*- coding: utf-8 -*-
"""
Завдання 4.4

Список vlans це список VLANів, зібраних з усіх пристроїв мережі, тому у списку
є номери VLAN, що повторюються.

Зі списку vlans потрібно отримати новий список унікальних номерів VLAN,
відсортований за зростанням номерів. Для отримання підсумкового списку не можна
видаляти конкретні vlanи вручну. У цьому випадку підсумковий список має
виглядати так:
[1, 2, 3, 4, 10, 20, 30, 100]

Записати підсумковий перелік унікальних номерів VLANів у змінну result. (саме
ця змінна перевірятиметься у тесті)

Отриманий список результату вивести на стандартний потік виведення (stdout) за
допомогою print.

Попередження: у розділі 4 тести можна легко "обдурити", зробивши потрібний
вивід print, без отримання результатів з даних завдання за допомогою Python. Це
не означає, що завдання зроблено правильно, просто на даному етапі складно
інакше перевіряти результат.
"""

vlans = [10, 20, 30, 1, 2, 100, 10, 30, 3, 4, 10]
print(sorted(list(set(vlans))))
