##########################################
reStructuredText и сложные документы.
##########################################
:date:  2014-08-30
:modified: 2014-12-08
:tags: reStructuredText, docutils, LibreOffice
:author: ДСМ
:summary: Использование reStructuredText в сложных документах.
:lang: ru
:translation: false

.. role:: bash(code)
   :language: bash

.. role:: rest(code)
   :language: rest

.. _Содержание:
.. contents:: Содержание
   :depth: 1

Почему и зачем
====================

"Давно хотелось"
-----------------

Давно хотелось освоить средство (назовём пока так, дабы не не путаться с языками, редакторами, процессорами....) для простой работы с обычными текстами (как большими так и маленькими), желательно в vim, с такими возможностями:

* отделение контента от форматирования;
* разбивка на "атомы" с возможностью повторного использования без копипастинга;
* простое создание форматированного текста;
* возможность создания "сложных" документов (с рисунками, таблицами, автооглавлением, перекрёстными ссылками, списком литературы);
* вывод в форматы doc(x), odt(ods), pdf, html, возможно Wiki и LaTeX (последний на практике использовать не приходилось, поэтому интерес чисто теоретический);
* использовать для документирования кода (python, про другие не думал, а в Delphi­Lazarus использовал javadoc­подобное документирование).

Почему reStructuredText
-----------------------

В качестве вариантов рассматривал reStructuredText, markdown, LaTeX, Wiki, LibreOffice Writer (с конвертацией куда надо), может что ещё было раньше (вроде DocBook) что отбросил сразу (сейчас не помню). Как по мне, reStructuredText подошёл для этих нужд наилучшим образом. Если кратко, почему не подходят другие.

* **markdown** слабоват, если не разбираться с каким‑либо из расширенных вариантов.
* **LaTeX** сложноват для просто набора текста, особенно если учесть, что LaTeX в чистом виде на практике мне не нужен.
* **LibreOffice Writer** использовал и продолжаю пока использовать как основной WYSiWYG текстовый процессор. Из него неплохо получается конвертировать в pdf и doc(x), чем и пользуюсь :), но остальные пожелания из `"Давно хотелось"`_ либо нереализуемы, либо требуют нетривиальных действий, на которые не хочется тратить время.
* **Wiki-подобная** разметка очень удобна для небольших текстов, но для описанных выше задач подходит слабо.

reStructuredText дополнительно к пожеланиям из `"Давно хотелось"`_ имеет **дополнительные плюсы** (как для меня, не скажу, что киллер­фичи, но приятно :))

* для программирования на python язык "родной".
* в vim уже встроена подсветка, а для более удобной работы есть замечательный `Rykka/riv.vim`_.
* `docutils`_ оказался довольно удобным и мощным. К слову, популярный pandoc отбросил сразу, так как он не собирает из разных "атомарных" частей через директиву *include.* 
* формулы (бывает нужно, не часто, но бывает).

Приступаем к работе
===================

Возникла задача создать довольно большой документ, который можно будет потом вывести и в LibreOffice writer (в определённом формате) и в html.

.. _structure:

Сразу создал структуру:

* для каждого раздела отдельную папку ./S01/ -- ./S13/;
* папку для рисунков ./img/;
* файл заголовков ./head.rst.
  
В каждой папке для разделов сохраняю каждый "атомарный" файл с "говорящим" названием. Например, ./S10/03.01.rst означает соответствующий уровень вложения. Глубже мне было не нужно. Файл заголовков содержит необходимые данные:

.. code-block:: rest

   .. |date| date:: %d.%m.%Y
   .. |time| date:: %H:%M

   .. sectnum::

   ######################################
   Системний аналіз економічних процесів.
   ######################################
       :Створено: |date| |time|
       :Авторський колектив: **Я** и др.

   ----

   .. contents:: Зміст.
       :backlinks: entry
       :depth: 4

 и небольшой скрипт, который соберет все вкучу:

.. code-block:: bash
   
    echo ".. include:: head.rst" > index.rst
    find ./S*/ -name "*.rst" | sort | sed 's|\.\/|..  iclude:: |g' >> index.rst

В результате получаем файл, index.rst из которого с помощью rst2html rst2odt получаем нужные форматы. Всё-бы хорошо, но есть несколько "но", решение которых в Интернете по-быстрому найти не получилось:

* `Формат в odt`_
* `Нумерация рисунков и таблиц`_

Формат в odt
=============

Для получение удобоваримого формата воспользовался инструкцией `styles-used-by-odtwriter`_ . Проблем особых не было (со стилями в офисах давно работаю). Но возникло несколько существенных моментов, которые пришлось "допиливать" через `StarBasic`_. Чтоб побыстрее воспользовался командой `запись макроса`_  (или `на хабре <http://habrahabr.ru/post/121149/>`_) и дальнейшей его правкой. Потом `поставил его на событие <https://help.libreoffice.org/Common/Events/ru>`_ открытие файла. Нужно было обновить оглавление и очистить форматы. Оглавление автоматически само не обновляется, а в заголовках рисунков  иногда "вылезало" кривое форматирование. Поэтому сначала каждый раз при открытии вручную проделывал указанные операции, потом решил автоматизировать. `Неплохая статья по этому поводу <http://www.script-coding.com/OOo/OOo_HelloWorld.html>`_ и `ещё один сайт <http://stackoverflow.com/questions/18755381/how-to-update-the-table-of-contents-in-an-odt-document-with-delphi-and-the-com>`_ по поводу обновления оглавления.

Текст макроса:

.. code-block:: vbnet

    sub Main
        dim document   as object
        dim dispatcher as object
        document   = ThisComponent.CurrentController.Frame
        dispatcher = createUnoService("com.sun.star.frame.DispatchHelper")
        dispatcher.executeDispatch(document, ".uno:UpdateCurIndex", "", 0, Array())
        dispatcher.executeDispatch(document, ".uno:SelectAll", "", 0, Array())
        dispatcher.executeDispatch(document, ".uno:ResetAttributes", "", 0, Array())
    end sub

``Макрос скорее всего "допилить" немного придется с учетом приведенных выше ссылок. Здесь пока как пример возможности. Пока для меня это не первостепенная задача. Если будет интересно, могу отладить и в отдельной статье описать подробнее.``

Ну это пол дела. Есть ещё пара задачек:

* `Нумерация рисунков и таблиц`_ Нужно не только в офисе, но и для любого выходного формата, поэтому рассмотрел в отдельном разделе.
* `Обычный текст с отступом`_ Задача оказалась довольно нетривиальной, поэтому тоже рассмотрел отдельно.

Нумерация рисунков и таблиц
============================

Думал, что не сильно нужно, но в процессе работы оказалось что ошибся. В Интернете готового решения не нашёл. Поэтому придумал своё.

В файл заголовков (см. `structure`_) добавил такие строчки:

.. code-block:: rest

   .. Figures
   .. |fig10010301| replace:: 10.1.
   .. |fig10030201| replace:: 10.2.
   .. |fig10030202| replace:: 10.3.

   .. Tables
   .. |tbl10030201| replace:: 10.1.

а в тексте ссылку записал таким образом:

.. code-block:: rest

   .. _fig10030201:
   .. figure:: img/SPPR.png
      :align: center

      Рис. |fig10030201|  Структура СППР.

**В итоге**:

* Нумерацию могу писать как угодно (с учётом раздела или сплошную для всего документа), причём, один раз. В принципе, если объектов много, можно разнести в отдельные файлы (например, figures.rst, tables.rst ...) и нумерацию автоматизировать.
* Если нужно добавить в раздел объект ссылочное имя ему нужно давать следующее, даже если объект вставляется между существующими. Например, если добавить в 10-й раздел 2-й рисунок файл заголовок изменится таким образом:

  .. code-block:: rest

     .. Figures

     .. |fig10010301| replace:: 10.1.

     .. |fig10030201| replace:: 10.2.
     .. |fig10030203| replace:: 10.3.
     .. |fig10030202| replace:: 10.4.

  Следить за таким файлом отдельно по каждному "атомарному файлу", не сложно. 

* Я получил простой, легко контролируемый способ нумерации объектов, который, как по мне, даже удобнее чем в родном LibreOffice.

Как дополнение, аналогично можно организовать `ссылки на литературу`__.

__ `Ссылка на литературу`_

Обычный текст с отступом
=========================

**В чем проблема.** Когда работаю со стилями в офисе для текста использую стиль "обычный текст", а остальные стили основываю на "базовый". Основные отличия:

* В `основном` стиле выравниваю по ширине, а в `базовом` по левому краю;
* В `основном` делаю отступ для первой строки, а в `базовом` без отступов.

docutils использует только rststyle-textbody. Вроде мелочь, сделал rststyle-textbody основным. Но после этого "поехало" форматирование в таблице, потом в полях, а потом, возможно, поедет ещё где-то. Пытаться создавать отдельно стили для таблиц, потом для полей, потом для того что ещё, может быть, поедет занятие бессмысленное. Тем более, что прикрутить эти стили задача тоже нетривиальная. Поэтому я решил сделать таким способом:

1. создать стиль rststyle-textbase;
2. обычный абзац форматировать именно этим стилем.

По поводу 1-го пункта вопросов нету, а со 2-м пришлось малость повозиться.

Сначала обычный текст просто поместил в контейнер: :code:`.. container:: textbase`. Сразу неудобства: первое - много писать (хотя, в vim можно и забиндить на hotkeys); второе - принципиальнее - текст нормально не подсвечивается.

Попытка сделать по-быстрому через :code:`.. |tt| replace:: .. container:: textbase` успехом не увенчалась, поэтому я решил проще. Добавил в начале каждого абзаца по "тт ", а потом в скрипте для сборки заменил на то, что нужно. "тт " а не "tt " потому что текст в основном печатается кириллицей (кстати, ещё один "+" этого метода). Это уже что-то, но писать в начале каждой строчки свои спецсимволы я посчитал тоже неправильным. Я решил, что простым текстом (в reStructuredText) можно считать все что начинается  большой буквы, а следующий абзац не содержит ничего.

В итоге скрипт для сборки сделал таким:

.. code-block:: bash

   echo ".. include:: head.rst"
   echo
   txt="..  container:: textbase\n    \n    "
   for f in `find ./S*/ -name "*.rst" -print | sort`
   do
       cat "$f" | sed '$ G' | sed ":a;/^[А-ЯІЇ]/N; s/^\([А-ЯІЇ]\)\([^\n]*\)\(\n$\)/""$txt""\1\2\n/g;ta" | sed "s/^тт /""$txt$""/g"
   done

Небольшой *комментарий:*

* :code:`sed '$ G'` -- добавил пустую строчку в конце, чтобы не потерять последний абзац;
* :code:`sed ":a;/^[А-Я]/N; s/^\([А-Я]\)\([^\n]*\)\(\n$\)/""$txt""\1\2\n/g;ta"` -- делаю нужную вставку для абзацев с кириллицей;
* :code:`sed "s/^тт /""$txt$""/g"` -- оставляю себе возможность, явно указать текст с отступом.

*Замечание:* 

* данный раздел касается пока только odt;
* такое решение не влияет на вывод для html;
* при необходимости для html вопрос решается элементарно созданием стиля `textbase.`

Ссылка на литературу
=====================

С учётом сказанного в разделе `Нумерация рисунков и таблиц`_ список литературы приобретает такой вид:

.. code-block:: rest

   .. |And98| replace:: 1
   .. |Wei11| replace:: 2

   .. _And98:

   |And98|. Andersson M.K. On the Effects of Imposing or Ignoring Long Memory When Forecasting // Working Paper Series in Economics and Finance, 1998. 

   .. _Wei11:

   |Wei11|. Weilkiens T. Systems Engineering with SysML/UML: Modeling, Analysis, Design. - Morgan Kaufmann, 2011

А ссылка на литературу принимает такой вид: :code:`[|Wei11|_]`

Ещё раз про рисунки в odt
==========================

Рисунки получаются довольно неплохо (я использую директиву :code:`.. figure::`). Сам рисунок помещается в кадр с заголовком. Ширина кадра рассчитывается по ширине рисунка. По идее, есть атрибут :code:`:figwidth:`, но задание этому атрибуту явного значения ничего на давало. Попытки изменить минимальную ширину в стиле `rststyle_figureframe` тоже ничего не дали.

Вопрос возник потому что плохо выглядит длинный заголовок для узкого рисунка. 

Потому, я решил вопрос по другому -- внёс изменения в файл: `docutils/writers/odf_odt/__init__.py`.

.. code-block:: python

   def generate_figure(self, node, source, destination, current_element):
       # ...
       width, height = self.get_image_scaled_width_height(node, source)

Заменил на

.. code-block:: python
   
   def generate_figure(self, node, source, destination, current_element):
       # ...
       if isinstance(node.parent, docutils.nodes.figure):
           width, height = self.get_image_scaled_width_height(node.parent, source)
       if width is None:
           width, height = self.get_image_scaled_width_height(node, source)

Теперь :code:`:figwidth:` работает так как мне нужно.

Выравнивание в таблицах
========================

Отсутствие выравнивания в таблицах существенный недостаток reStructuredText. Пока в этот вопрос не углублялся. Нашёл `итересный ресурс <http://mbless.de/4us/typo3-oo2rest/06-The-%5Bfield-list-table%5D-directive/1-demo.rst.html>`_ по этому поводу. Насколько понял, официально в docutils этот инструмент в ближайшее время вряд ли попадёт -- есть некоторые неоднозначности и действия "по умолчанию", с которыми не согласны авторы docutils.

Для себя решил по быстрому (костылём). В принципе, в самой таблице можно явно указать стиль: :code:`.. container:: centeredtextbody` (такой стиль есть по умолчанию), а для того, чтобы получить объединённые ячейки в заголовках использую grid-таблицу. В этом случае использование контейнера делает таблицу центрированный столбец очень широким. Вот если бы можно было задавать ширину столбцов (для директивы :code:`.. table::` такого не предусмотрено). Для этого вношу изменение в файл `docutils/parsers/rst/directives/tables.py`. В класс :code:`class RSTTable(Table)` добавляю опцию:

.. code-block:: python
   
   option_spec = {'widths': directives.positive_int_list,
                  'class': directives.class_option,
                  'name': directives.unchanged}

а в функцию :code:`def run(self)`, этого класса дописываю фрагмент:

.. code-block:: python

   if 'widths' in self.options and len(table_node.children) == 1:
       col_widths = self.options['widths']
       for i in range(len(table_node.children[0].children)):
           if len(col_widths) == 0: break
           if table_node.children[0].children[i].tagname == 'colspec':
               table_node.children[0].children[i]['colwidth'] = col_widths.pop(0)

**З.Ы.**

Сейчас кое-что переделал (возможности оставил те же, изменил (унифицировал) реализацию и настройку).

Об этом в следующей статье на эту тему (Когда напишу вставлю ссылку).




.. _styles-used-by-odtwriter: http://docutils.sourceforge.net/docs/user/odt.html#styles-used-by-odtwriter
.. _StarBasic: https://wiki.openoffice.org/wiki/API/Tutorials/StarBasic
.. _запись макроса: https://help.libreoffice.org/Common/Recording_a_Macro/ru
.. _Rykka/riv.vim: https://github.com/Rykka/riv.vim
.. _docutils: http://docutils.sourceforge.net/
