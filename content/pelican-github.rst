#############################
Переселяем pelican на github.
#############################
:date: 2014-12-15
:modified: 2015-07-10
:tags: blog, pelican, github
:category: веб
:slug: pelican-github
:author: ДСМ
:summary: Рассматривается работа в github на примере статического блога dsmblog, описанного в предыдущих статьях.
:lang: ru
:translation: false
:keywords:

.. role:: py(code)
   :language: python

.. role:: bash(code)
   :language: bash

.. role:: rest(code)
   :language: rest

.. _Содержание:
.. contents:: Содержание
   :depth: 1

Предисловие
===========

В предыдущих статьях, посвящённых генератору статических сайтов pelican были описаны основные `задачи и цели <|todo|>`_, которые хотел решить работая с пеликаном, о описаны `начальные действия <|minstart|>`_ необходимые для того чтобы создать свой блог, поместить в нём пару статей и запустить на локальном сервере.

Следующим шагом, по плану, необходимо разместить проект на каком-либо хостинге для проектов, а результат на веб‑хостинге.

Что нужно сделать
------------------

Итак, ориентировочный перечень задач:

* Создать новый проект на github.
* Перенести код проекта dsmblog в созданный проект.
* Настроить синхронизацию.
* Разместить результат на github.io.
* Настроить синхронизацию для результирующего блога с хостингом.

Почему git
----------

Выбор, в общем-то, между `github <https://github.com/>`_ и `bitbucket <https://bitbucket.org/>`_. Оба хостинга имеют необходимый бесплатный функционал (мне пока нужно git и веб‑хостинг, возможность работать через SSL есть и там, и там). Субъективные оценки интерфейса старался не учитывать. Для себя отметил пока такие особенности ресурсов:

github

* имеет большое сообщество;
* не ограничивает количество человек в команде;
* не даёт права создавать бесплатные закрытые проекты;
* много маститых разработчиков размещают свои официальные репозитории на этом сервисе.

bitbucket

* предоставляет возможность создавать до пяти бесплатных приватных проектов (основное преимущество);
* ограничивает количество разработчиков для бесплатных проектов;
* сообщество довольно большое, хоть и поменьше чем у github;
* По маститости, вроде как поскромнее чем github.

В общем, если нужен приватный проект − однозначно bitbucket, в противном случае − скорее github.

Так как прятать dsmmblog я не планирую, решил разместить на github.

`Содержание`_

Перенос dsmblog на github
===========================

Регистрация и установка git.
----------------------------

Если ещё раньше этого сделано не было (регистрация на github и | или установка git) − самое время.

`Регистрация на github <https://help.github.com/articles/signing-up-for-a-new-github-account/>`_ предельно проста, хорошо описана (хоть и на английском, но понятно для того чтобы выбрать бесплатный вариант для обычного пользователя).

`Установка git <https://help.github.com/articles/set-up-git/#platform-linux>`_ довольно проста (по крайней мере, в Linux). По поводу :bash:`git config` −изменения записываются в файл :bash:`~/.gitconfig` и могут легко быть исправлены и (или) дополнены. Более того, можно сразу создать (или скопировать из архива) этот файл.

Мой файл конфигурации:

.. code-block:: bash

   [user]
       name = UserName  # user name
       email = User@e.mail  # email address that will be associated with your Git commits
   [core]
       autocrlf = input  # settings for CRLF conversion 
       safecrlf = true  #  settings for CRLF conversion 
       excludesfile = ~/.gitexcludes  # like .gitignore but for all projects
   [credential]
       helper = cache --timeout=3600  # allow to input username and password once per timeout
   [user]
       name = ДСМ  # user name
       email = dmitry.5674@gmail.com  # email address that will be associated with your Git commits
   [core]
       autocrlf = input  # settings for CRLF conversion 
       safecrlf = true  #  settings for CRLF conversion 
       excludesfile = ~/.gitexcludes  # like .gitignore but for all projects
   [credential]
       helper = cache --timeout=3600  # allow to input username and password once per timeout

Есть вопрос выбора между SSL и HTTPS. Первый вариант (SSL), вроде даёт возможность не вводить каждый раз пароль и под Linux реализуется элементарно. Второй (HTTPS) рекомендован githib-ом + в комбинации с параметром :bash:`helper = cache --timeout=3600` позволяет вводить пароль только один раз за сеанс работы. В итоге я остановился на HTTPS (пошёл по пути наименьшего сопротивления).

`Содержание`_

Хостим код на github
--------------------

Вариант очевидный. Есть локальный dsmblog и есть одноимённый проект на github. Нужно синхронизировать. Можно, но сложно. Хотя, если на github совсем пустой проект, то не так уж и сложно. Но, как сказал классик, мы пойдём другим путём.

Сохраняем свой проект под другим именем (например, dsmblog_local):

.. code-block:: bash

   mv dsmblog dsmblog_local

Клонируем проект с github и инициализируем:

.. code-block:: bash

   git clone https://github.com/dmisem/dsmblog.git && cd dsmblog && git init

Копируем проект:

.. code-block:: bash

   cp -rf ../dsmblog_local/* ./

Почти всё. Осталось настроить параметры синхронизации (назовём это так). Об этом в следующем подразделе.

Локальные параметры
-------------------

Локальные параметры:
* некоторые параметры из :bash:`pelicanconf.py`, которые не нужно выкладывать в общедоступную среду;
* настройки :bash:`.gitignore`, указывающие какие файлы не будут учитываться git и, соответственно, не будут залиты на github.

Фрагмент :bash:`pelicanconf.py`, которые "подтягивают" данные из файла :bash:`local_settings.py`:

.. code-block:: python

   import local_settings as ls

   AUTHOR = ls.AUTHOR
   SITENAME = ls.SITENAME
   SITEURL = ls.SITEURL
   PATH = ls.PATH
   TIMEZONE = ls.TIMEZONE
   LOCALE = ls.LOCALE
   DEFAULT_LANG = ls.DEFAULT_LANG
   
Что должно быть в :bash:`local_settings.py`, по моему, очевидно.

При работе с python3.4 возник нехороший нюанс - :py:`import` не подтягивает фалы, которые расположены в той же папке, что и :bash:`pelicanconf.py`, решается явным добавлением пути проекта в :py:`sys.path`:

.. code-block:: python

   import os
   import sys
   SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
   sys.path.append(SITE_ROOT)
   import local_settings as ls

Мой :bash:`.gitignore`:

.. code-block:: bash

   # Generated by vim
   .ropeproject/
   __pycache__/

   # Generated by pelican
   # Folder output changed to dsmblog
   #   for pushing into gh-pages branch.
   cache/
   output/
   /dsmblog/

   # temporary files
   *.pid
   test*
   tmp*
   *.pyc

   # local settings
   local_settings.*
   Makefile
   fabfile.py

Здесь считаю нужным отметить папки `output/` и `/dsmblog/`. На github хранится только код без результирующего сайта, Сам итоговый сайт будет размещён отдельно (подробнее в следующем разделе. Для этого потом папку `output/` нужно будет переименовать в `/dsmblog/`.

Заливаем код
------------

Добавляем свои файлы в индекс git:

.. code-block:: bash

   git add .

Коммитим изменения (параметр `-m` если коммитятся только изменения или добавления, для коммита также и удалений нужно использовать  `-a`) и "пушим" (отправляем) изменения на github:

.. code-block:: bash

   git commit -m "first commit all project to github."
   git push

Проходим авторизацию (если не используем SSL), заходим на сайт https://github.com и авторизируемся (или обновляем страницу если уже там) и наблюдаем изменения.

github как веб-хостер
=======================

Веб-хостинг для проектов github располагается на сайте https://pages.github.com сайты называются Pages, подробная справка по адресу https://help.github.com/categories/github-pages-basics/.

Поддерживаются два типа страниц: страница пользователя (вариант с организацией я не рассматриваю) и страница проекта. Страницы (любого типа) можно создать (и потом редактировать) с помощью неплохого, простого генератора, который имеет небольшое количество довольно симпатичных шаблонов (правда, не отзывчивых).

В учебно-практических целях остановился на таком варианте:

* создаю персональный сайт, где размещаю краткую информацию о себе и ссылки на свои проекты;
* создаю сайт проекта dsmblog куда помещаю созданный статический блог.

Персональный сайт
-----------------

Персональный сайт решил сделать с помощью встроенного генератора.

Для этого строго по `инструкции <https://help.github.com/articles/creating-pages-with-the-automatic-generator/>`_ создаю проект dmisem.github.io, и для нового проекта создаю сайт с помощью генератора (потом изменить с помощью генератора можно зайдя в меню Settings).

На первом этапе корректируем на языке Markdown (сайт содержит довольно подробную инструкцию по markdown) наполнение, созданное генератором. На втором выбираем шаблон. Через несколько минут сайт будет доступен по адресу http://dmisem.github.io/

Статический блог (страницаа проекта).
-------------------------------------

Суть создания страницы проекта − создание независимой ветки gh-pages и размещение там статического сайта.

Самый простой способ - создать страницу с помощью генератора (через команду меню Settings). Заодно можно посмотреть что содержит стандартная страница.

Далее клонируем ветку внутрь папки проекта (таким образом внутри папки dsmblog будет создана ещё одна папка dsmblog) и инициализируем её:

.. code-block:: bash

   git clone -b gh-pages https://github.com/dmisem/dsmblog.git && cd dsmblog && git init

и вычищаем старое содержимое:

.. code-block:: bash

   git rm -rf . && git commit -a "clear old content" && git push

Теперь возвращаемся в основной каталог и генерируем сайт во вновь созданную папку:

.. code-block:: bash

   pelican -o dsmblog content

Теперь записываем изменения на github:

.. code-block:: bash

   cd dsmblog && git add . && git commit -m "generated on timestamp" && git push

Всё! Можно заходит на сайт http://dmisem.github.io/dsmblog/

`Содержание`_

Автоматизация и синхронизация
==============================

Автоматизировать внесение изменений кода на github смысла не вижу.

А вот работу с созданным сайтом вижу по такой схеме: 

* сначала создаётся сайт в папке output;
* проверяется его работа на локальном сервере;
* если все в порядке, создаётся окончательная версия в папке dsmblog и отправляется на сервер.

Автоматизировать стоит только последний пункт. Для этого создан скрипт `git.dsmblog.sh` с таким содержим:

.. code-block:: bash

   #!/usr/bin/env bash

   DIR=`pwd`"/dsmblog"
   CDT=`date +%Y-%m-%d\ %H:%M`  # Current datetime
   GT="git --git-dir=${DIR}/.git --work-tree=${DIR} "

   pelican -o dsmblog content
   echo Generated
 
   ${GT}add . && ${GT}commit -a -m "Autogenerate: ${CDT}" && ${GT}push
   echo Pushed!

`Содержание`_

.. |todo| replace:: dsmblog-todo.html
.. |minstart| replace:: pelican-minstart.html
