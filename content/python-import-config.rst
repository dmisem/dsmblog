#####################################
Импорт конфигурационных файлов python
#####################################
:date: 2015-07-09
:modified: 2015-07-09
:tags: python
:category: python
:slug: python-import-config
:author: ДСМ
:summary: Рассматривается использование конфигурационных файлов написанных на python через механизм импортирования модулей.
:lang: ru
:translation: false
:keywords:

.. role:: rest(code)
   :language: rest

.. role:: py(code)
   :language: python

Продолжаю (после перерыва) заметки для себя. Сейчас немного из области изучения python.

Словари в python видятся мне как очень удобный инструмент для ведения конфигурационных файлов (любого вида, любой вложенности). Например, такого типа:

.. code-block:: python

   Confg = {'num': 1,
            'text': 'there is a text',
            'list': [1, 2, (2, 3)],
            'dict': {'d1': 123, 'd2': 'werwe'}}

Допустим, что такие файлы расположены в некоторой папке (т.е. в папке может быть нескольео питоновских файлов, и в каждом файле несколько конфигурационных объектов, предположительно словарей, но, в принципе, любых). Нужно собрать их вместе в один словарь.

Покопавшись в доках (получилось поработать со стандратной документацией благодаря ограниченному доступу к Интернету) понял, что нужно использовать функцию :py:`import_module` из модуля :py:`importlib`. Предварительно нужно добавить папку в пути поиска инструкции import (список :py:`sys.path`)

Если учесть возможность использования генераторов, получается такой довольно компактный "питонистичный" код:

.. code-block:: python

   from os import listdir
   from os.path import isdir
   from sys import path as sp
   from importlib import import_module as im


   def _main():
       # Берём некую папку (с проверкой существования)
       PApp = r'/home/dsm/prg/python/set_proxy/app_cfg'
       if not isdir(PApp): return {}

       # Получаем список py файлов в папке PApp,
       # и если не найдено выходим,
       # если найдено - добавляем в пути поискa и импортируем
       apps = [f for f in listdir(PApp) if f.endswith('.py')]
       if not apps: return {}
       sp.append(PApp)
       g = {m.__name__:
            {o: m.__getattribute__(o) for o in dir(m) if not o.startswith('_')}
            for m in [im(a[:-3]) for a in apps]}
       return g


   if __name__ == "__main__":
       d = _main()
       if d:
           for (m, a) in d.items(): print('{0} => {1}'.format(m, a))
       else:
           print('not found')
