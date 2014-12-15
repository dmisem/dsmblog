###################
Запускаем пеликана.
###################
:date:  2014-11-30 17:20
:modified: 2014-11-26 17:20
:tags: blog, pelican, start
:category: веб
:slug: pelican-minstart
:author: ДСМ
:summary: Установка, минимальная настройка pelican − инструмента для создание статических блогов, использующего python, Jinja2, ReStructuredText или Markdown.
:lang: ru
:translation: false

.. role:: bash(code)
   :language: bash

.. role:: rest(code)
   :language: rest

.. _Содержание:
.. contents:: Содержание
   :depth: 1

Предисловие
===========

В статье "`Задачи и цели проекта`_" были изложены мотивы, побудившие заняться пеликаном, определены задачи и цели, намечены основные шаги.

Что такое пеликан, его возможности, и довольно подробная документация находится на официальном сайте документации pelican_.

Пока переводить её не планирую.

Поэтому в этой статье рассмотрим первый шаг − старт пеликана. И особенности, которые возникли в моём случает.

`Содержание`_

Установка
=========

Установка довольно простая. Через pip.

Поэтому, сначала создаём виртуальное окружение (я использую `virtualenvwrapper <http://virtualenvwrapper.readthedocs.org/>`_): 

.. code-block:: bash

   mkvirtualenv -a blog_project_path pelican

Устанавливаем pelican:

.. code-block:: bash
   
   pip install pelican

или последнюю версию с `github <https://github.com/getpelican/pelican>`_:

.. code-block:: bash
   
   pip install -e "git+https://github.com/getpelican/pelican.git#egg=pelican"


Необходимо определиться с языком разметки для написания статей (ReStructuredText или Markdown). Markdown более популярен, так как несколько проще, но менее функционален. Я использую ReStructuredText, так нужны были его возможности (таблицы, include), потом установил `riv <https://github.com/Rykka/riv.vim>`_ и работать с текстом в `vim <http://www.vim.org/>`_ стало совсем удобно. К тому же, ReStructuredText используется `sphinx <http://sphinx-doc.org/>`_ для документирования кода в python (для генерирования документации). Пока документацию не генерировал, но ближайшем будущем к этому приду. Так что для меня вопроса с выбором ReStructuredText или Markdown не стоит. Markdown возможно установлю в будущем, чтобы поработать с его синтаксисом.

Так как я sphinx пока не использую достаточно docutils (его устанавливать не нужно, он идет в зависимостях пеликана).

Для выбравших Markdown:

.. code-block:: bash

   pip install markdown

Для начала работы все готово!

`Содержание`_

Первый блог
============

.. contents:: Содержание
   :depth: 1
   :backlinks: top
   :local:

Создаем каркас проекта
----------------------

Каркас создается простой командой:

.. code-block:: bash
   
   pelican-quickstart

Один важный момент. Если виртуальное окружение привязано к директории проекта (в папке окружения лежит файл .project, в котором указан соответствующая директория), то пеликан создаст каркас именно в этой директории независим от того, какая директория является текущей. Если возникает потребность создать второй блог, то нужно либо создавать ещё одно окружение, либо отвязывать окружение от папки проекта, либо согласовывать папки (или переименовать папку со старым блогом, или изменить папку проекта окружения).

Теперь нужно ответить на вопросы (в принципе настройки потом можно поменять)

.. code-block:: bash

   Welcome to pelican-quickstart v3.4.0.

   This script will help you create a new Pelican-based website.

   Please answer the following questions so this script can generate the files
   needed by Pelican.
    
   Using project associated with current virtual environment.Will save to:
   /home/***********

   > What will be the title of this web site? dsmblog
   > Who will be the author of this web site? ДСМ
   > What will be the default language of this web site? [en] ru
   > Do you want to specify a URL prefix? e.g., http://example.com   (Y/n) 
   > What is your URL prefix? (see above example; no trailing slash) http://localhost:8000
   > Do you want to enable article pagination? (Y/n) 
   > How many articles per page do you want? [10] 
   > Do you want to generate a Fabfile/Makefile to automate generation and publishing? (Y/n) 
   > Do you want an auto-reload & simpleHTTP script to assist with theme and site development? (Y/n) 
   > Do you want to upload your website using FTP? (y/N) 
   > Do you want to upload your website using SSH? (y/N) 
   > Do you want to upload your website using Dropbox? (y/N) 
   > Do you want to upload your website using S3? (y/N) 
   > Do you want to upload your website using Rackspace Cloud Files? (y/N) 
   > Do you want to upload your website using GitHub Pages? (y/N) 
   Done. Your new project is available at /home/*********

Пара замечаний:

* Выбор языка по умолчанию. У меня выбор между английским, русским и украинским.
  Английский я, к сожалению, знаю не на столько, чтобы на нем писать статьи.
  Если выбирать между русским и украинским, то тут определяющими факторами есть 
  то, что русскоговорящее сообщество значительно больше, 
  и то, что планирую попытаться сделать авто-перевод статей и предполагаю, что с русского будет качественней
  (хотя по этому поводу собираюсь изучить вопрос попозже).
* URL prefix лучше указывать даже если пока сайт будет работать на localhost.
  Иначе будет выдаваться предупреждение (warning)
* Автоматизацию генерирования и публикации взял по умолчанию (автообновление сайта при внесении удобно).
  Автообновление сайта при внесении изменений удобно,
  а публикацию в вебе рассмотрю позже.
* Остальные параметры можно установить по умолчанию (или поменять на своё усмотрение).
  В любом случае, их легко можно поменять позже.

В результате получим такую структуру:

.. code-block:: bash

   dsmblog/
   ├── content/
   │   └── (pages)
   ├── output/
   ├── Makefile
   ├── develop_server.sh
   ├── fabfile.py
   ├── pelicanconf.py       # Main settings file
   └── publishconf.py       # Settings to use when ready to publish

Теперь можно сгенерировать блог:

.. code-block:: bash
   
   pelican content

Переходим в папку output/ и запускаем сервер (для python3):

.. code-block:: bash
   
   python -m http.server

или (для python2):

.. code-block:: bash
   
   python -m SimpleHTTPServer

или (пеликан сам определит что и как запускать):

.. code-block:: bash
   
   python -m pelican.server

Теперь в броузере по адресу http://127.0.0.1:8000 можем посмотреть свой пустой блог.

В дальнейшем удобнее использовать скрипт

.. code-block:: bash

   develop_server.sh start

В этом случае все изменения в наполнении и установка блога будут вноситься автоматически. Иногда, правда, если где-то сделана ошибка и на сайте (блоге) изменеия не отображаются, можно остановить сервер :bash:`develop_server.sh stop`, пересобрать блог :bash:`pelican content` (обращая внимание на текущую папку) и заново запустить сервер.

`Первый блог`_

Создаем первую статью
---------------------

Пример можно взять с сайта документации pelican_, там же достаточно подробная инофрмация о по поводу наполнения статей. В том числе, ссылки на статические ресурсы вроде изображений, файлов pdf и т.п.

Создаем файл с расширением .rst, наппример, my-super-post.

Вносим метаданные и какой-нибудь текст

.. code-block:: rest

   My super title
   ##############
   
   :date: 2010-10-03 10:20
   :modified: 2010-10-04 18:40
   :tags: thats, awesome
   :category: yeah
   :slug: my-super-post
   :authors: Alexis Metaireau, Conan Doyle
   :summary: Short version for index and feeds
   
   Какой-нибудь текст для моей первой супер-статьи.

Если запущен :bash:`develop_server.sh`, то просто обновляем страницу, если какой другой, то сначала перегенерируем сайт.

Потом эту супер-страницу можно будет перезаписать, удалить или спрятать (:rest:`:status: hiiden`)

`Первый блог`_

Устанавливает тему
------------------

Для работы с темами в пеликане есть инструмент :bash:`pelican-themes`, с помощью которого можно как установить готвые темы и использовать их потом только по названию. Или же можно использовать абсолютные или относительные (относительно папки проекта, например, :bash:`themes/pelican-bootstrap3`) пути к темам, которые содержат необходимые шаблоны.

Можно шаблон использовать разово, собрав сайт с параметром :bash:`-t`:

.. code-block:: bash

   pelican -t theme_or_path_to_theme content

или, если тема будет использоваться постоянно, добавить параметр :bash:`THEME` в файле настроек :bash:`pelicanconf.py`. Например, 

.. code-block:: python

   THEME = "themes/pelican-bootstrap3"

При этом нужно, чтобы был установлен параметр

.. code-block:: python

   RELATIVE_URLS = True

Довольно большой перечень шаблонов можно найти на `хабе <https://github.com/getpelican/pelican-themes>`_.

Для себя хотел адаптивный шаблон, поэтому выбрал `pelican-bootstrap3 <https://github.com/DandyDev/pelican-bootstrap3>`_

Опять же, возможные вариаты установки хорошо описаны а сайте. Как вариант скопировать в подпапку проекта :bash:`themes` 

.. code-block:: bash

   cd themes
   https://github.com/DandyDev/pelican-bootstrap3.git

и прописать как узано выше путь к файлу. В этом случае тема будет только для этого блога.

Другой вариант установить тему в виртуальное окружение pelican (так я его назвал в начале статьи), потом установить через :bash:`pelican-themes` и подключать только по названию. В этом случае, легко можно создавать несколько блогов в одном окружении с этой темой.



`Первый блог`_

Конфигурируем
-------------

Конфигурация блога задается с помощью параметров (переменных) в файле ``pelicanconf.py``. Полный перечень переменных определяется темой.

Сущестувует рекомендация разделять файл конфигурации, во-первых, для обеспечения конфиденциальности (персональные данные хранить в отдельном файле и не синхронизировать их с хостингом (включить в ``.gitignore``)), во-вторых, при большом объему логически разделять.

Пока для себя необходимости такой не вижу. Поэтому глубже рассмотрю этот вопрос в другой раз.

В целом, переменные, которые идут по умолчанию впполне понятны сами по себе. Часть из них устанавливается во время сздания каркаса, часть уже правили когда тему устанавливали.

Поэтому, суть конфигурирования (на начальном этапе) посмотреть параметры и установить свои данные. Добавить (при желании), свои контакты с соц. сетях и т.п.

**На этом пока все.**

`Первый блог`_

`Содержание`_

.. _pelican: http://docs.getpelican.com
.. _`Задачи и цели проекта`: dsmblog-todo.html
