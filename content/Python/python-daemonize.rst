#####################################
Демонизация на python3
#####################################
:date: 2015-07-13 07:49:51
:modified: 2015-07-13 07:50:22
:tags: python, декораторы
:author: ДСМ
:summary: Создание утилиты для демонизации программ написанных на python разными способами.
:lang: ru
:translation: false


В процессе решения одной задачи возникла необходимость демонизировать одну довольно простую программу, которая должна повторятся в фоне бесконечно через определённые промежутки времени. В статье описано последовательность решения поставленной задачи. Получилось довольно много кода, результат выложен на `гитхабе`_.

Так как изучаю python решил поискать (написать) утилитку для выполнения этой задачи. Покопавшись в недрах Интернета, нашёл класс который неплохо справляется с этой задачей (к сожалению, ссылку на сайт не сохранил). После того, как адаптировал код к python3, получил такой класс:

.. raw:: html

   <details> <summary>посмотреть код</summary>

.. code-block:: python

   class Daemon:
       """
       A generic daemon class.

       Usage: subclass the Daemon class and override the run() method
       """
       def __init__(self, pidfile, stdin='/dev/null',
                    stdout='/dev/null', stderr='/dev/null'):
           self.stdin = stdin
           self.stdout = stdout
           self.stderr = stderr
           self.pidfile = pidfile

       def daemonize(self):
           """
           do the UNIX double-fork magic,
           see Stevens' "Advanced Programming in the UNIX Environment"
           for details (ISBN 0201563177)
           http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
           """
           try:
               pid = os.fork()
               if pid > 0:
                   # exit first parent
                   exit(0)
           except(OSError) as e:
               stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
               exit(1)

           # decouple from parent environment
           os.chdir("/")
           os.setsid()
           os.umask(0)

           # do second fork
           try:
               pid = os.fork()
               if pid > 0:
                   # exit from second parent
                   exit(0)
           except(OSError) as e:
               stderr.write("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
               exit(1)

           # redirect standard file descriptors
           stdout.flush()
           stderr.flush()
           si = open(self.stdin, 'r')
           so = open(self.stdout, 'a+')
           se = open(self.stderr, 'a+')
           os.dup2(si.fileno(), stdin.fileno())
           os.dup2(so.fileno(), stdout.fileno())
           os.dup2(se.fileno(), stderr.fileno())

           # write pidfile
           register(self.delpid)
           pid = str(os.getpid())
           open(self.pidfile, 'w+').write("%s\n" % pid)

       def delpid(self):
           os.remove(self.pidfile)

       def start(self):
           """
           Start the daemon
           """
           # Check for a pidfile to see if the daemon already runs
           try:
               with open(self.pidfile, 'r') as pf:
                   pid = int(pf.read().strip())
           except(IOError):
               pid = None

           if pid:
               message = "pidfile %s already exist. Daemon already running?\n"
               stderr.write(message % self.pidfile)
               exit(1)

           # Start the daemon
           self.daemonize()
           self.run()

       def stop(self):
           """
           Stop the daemon
           """
           # Get the pid from the pidfile
           try:
               with open(self.pidfile, 'r') as pf:
                   pid = int(pf.read().strip())
           except(IOError):
               pid = None

           if not pid:
               message = "pidfile %s does not exist. Daemon not running?\n"
               stderr.write(message % self.pidfile)
               return  # not an error in a restart

           # Try killing the daemon process
           try:
               while 1:
                   os.kill(pid, SIGTERM)
                   sleep(0.1)
           except(OSError) as err:
               err = str(err)
               if err.find("No such process") > 0:
                   if os.path.exists(self.pidfile):
                       os.remove(self.pidfile)
               else:
                   print(err)
                   exit(1)

       def restart(self):
           """
           Restart the daemon
           """
           self.stop()
           self.start()

       def run(self):
           """
           You should override this method when you subclass Daemon.
           It will be called after the process has been
           daemonized by start() or restart().
           """

.. raw:: html

   </details><br />

Проверил, работает ничего, но пользоваться регулярно неудобно. Поэтому решил добавить функцию, которая будет за меня (как пользователя этой утилитой) создавать класс-реализацию и "прикручивать" функцию, которую нужно демонизировать а также выполнять действия 'start', 'stop' или 'restart'. Результат:

.. raw:: html

   <details> <summary>посмотреть код</summary>

.. code-block:: python

   def daemon_exec(func, action, pidfile, **std):
       if action not in DMN_Actions: return
       DMN_Actions[action](pidfile, func, **std)


   DMN_Actions = {
       'start': daemon_start,
       'stop': daemon_stop,
       'restart': daemon_restart}


   def daemon_start(pidfile, func, **std):
       class DmnDecor(Daemon):
           def run(self):
               func()
       DmnDecor(pidfile, **std).start()


   def daemon_stop(pidfile, func=None, **std):
       Daemon(pidfile, **std).stop()


   def daemon_restart(pidfile, func, **std):
       class DmnDecor(Daemon):
           def run(self):
               func()
       DmnDecor(pidfile, **std).restart()

.. raw:: html

   </details><br />

Теперь этим можно уже пользоваться. Например, так:

.. raw:: html

   <details> <summary>посмотреть код</summary>

.. code-block:: python

   #! /usr/bin/python3
   from sys import argv
   from os import getenv
   from os.path import join
   from dsm_pytools.daemon import daemon_exec
   from time import sleep


   fn = join(getenv('HOME'), 'daemon_example')
   out = {'stdout': fn + '.log'}
   action = None if len(argv) == 1 else argv[1]


   def dmn_example(*arg):
       while True:
           print('testing daemon ...')
           sleep(5)


   daemon_exec(dmn_example, action, fn + '.pid', **out)

.. raw:: html

   </details><br />

Так как аппетит приходит во время еды, добавим немного "сахара" в виде декораторов. Для лучшего понимания декораторов в python можно порекомендовать одну статью, точнее, это `развернутый ответ на stackoverflow.com`_. Переводов в Интернете гуляет немало, например, `на хабре`_.

Получили такую вот функцию:

.. raw:: html

   <details> <summary>посмотреть код</summary>

.. code-block:: python

   def daemon_decor(pidfile, **std):

       def decor(func):

           def act(action):
               res = daemon_exec(func, action, pidfile, **std)
               return res
           return act
       return decor

.. raw:: html
   
   </details><br />

Теперь использовать более "красиво":

.. raw:: html

   <details> <summary>посмотреть код</summary>

.. code-block:: python

   #! /usr/bin/python3
   from sys import argv
   from os import getenv
   from os.path import join
   from dsm_pytools.daemon import daemon_decor
   from time import sleep


   fn = join(getenv('HOME'), 'daemon_example')
   out = {'stdout': fn + '.log'}
   action = None if len(argv) == 1 else argv[1]


   @daemon_decor(fn + '.pid', **out)
   def dmn_example():
       while True:
           print('testing daemon ...')
           sleep(5)


   dmn_example(action)

.. raw:: html
   
   </details><br />

И последний момент, который захотелось реализовать − автоматизировать повтор действия. До сих пор, демонизируется функция, в которой выполняется бесконечный цикл. Почему бы и этот цикл не завернуть в декоратор:

.. raw:: html

   <details> <summary>посмотреть код</summary>

.. code-block:: python

   def repeat_daemon_decor(sleep_time, pidfile, times=0, **std):

       def decor(func):

           def new_func():
               i = 1
               while (not times) or (i <= times):
                   func()
                   sleep(sleep_time)
                   i += 1

           def act(action):
               res = daemon_exec(new_func, action, pidfile, **std)
               return res

           return act
       return decor

.. raw:: html
   
   </details><br />

Теперь использовать его сущее удовольствие:

.. raw:: html

   <details> <summary>посмотреть код</summary>

.. code-block:: python

   #! /usr/bin/python3
   from sys import argv
   from os import getenv
   from os.path import join
   from dsm_pytools.daemon import repeat_daemon_decor as rdd


   fn = join(getenv('HOME'), 'daemon_example')
   out = {'stdout': fn + '.log'}
   action = None if len(argv) == 1 else argv[1]


   @rdd(5, fn + '.pid', **out)
   def dmn_example():
       print('testing daemon ...')


   dmn_example(action)

.. raw:: html
   
   </details><br />

И в завершение, для общедоступности разместил результат (свёл всё вместе, добавил обработку исключения ...) на `гитхабе`_.

.. Links:
.. _`гитхабе`: https://github.com/dmisem/dsm_pytools
.. _`развернутый ответ на stackoverflow.com`: http://stackoverflow.com/questions/739654/how-can-i-make-a-chain-of-function-decorators-in-python
.. _`на хабре`: http://habrahabr.ru/post/141411/
