# Практика 4. Прикладной уровень

## Программирование сокетов: Прокси-сервер
Разработайте прокси-сервер для проксирования веб-страниц. 
Приложите скрины, демонстрирующие работу прокси-сервера. 

### Запуск прокси-сервера
Запустите свой прокси-сервер из командной строки, а затем запросите веб-страницу с помощью
вашего браузера. Направьте запросы на прокси-сервер, используя свой IP-адрес и номер порта.
Например, http://localhost:8888/www.google.com

_(*) Вы должны заменить стоящий здесь 8888 на номер порта в серверном коде, 
то есть тот, на котором прокси-сервер слушает запросы._

Вы можете также настроить непосредственно веб-браузер на использование вашего прокси сервера. 
В настройках браузера вам нужно будет указать адрес прокси-сервера и номер порта,
который вы использовали при запуске прокси-сервера (опционально).

### А. Прокси-сервер без кеширования (4 балла)
1. Разработайте свой прокси-сервер для проксирования http GET запросов от клиента веб-серверу 
   с журналированием проксируемых HTTP-запросов. В файле журнала сохраняется
   краткая информация о проксируемых запросах (URL и код ответа). Кеширование в этом
   задании не требуется. **(2 балла)**
2. Добавьте в ваш прокси-сервер обработку ошибок. Отсутствие обработчика ошибок может
   вызвать проблемы. Особенно, когда клиент запрашивает объект, который не доступен, так
   как ответ 404 Not Found, как правило, не имеет тела, а прокси-сервер предполагает, что
   тело есть и пытается прочитать его. **(1 балл)**
3. Простой прокси-сервер поддерживает только метод GET протокола HTTP. Добавьте
   поддержку метода POST. В запросах теперь будет использоваться также тело запроса
   (body). Для вызова POST запросов вы можете использовать Postman. **(1 балл)**

Приложите скрины или логи работы сервера.

#### Демонстрация работы
Логи при запросе к ральной странице и к ошибочной:
```
2026-03-31 13:29:59,702 INFO URL: http://spbu.ru, Response Code: 200
2026-03-31 13:29:59,738 ERROR Error while requesting http://themes/spbgu/markup/dist/manifest.json: HTTPConnectionPool(host='themes', port=80): Max retries exceeded with url: /spbgu/markup/dist/manifest.json (Caused by NameResolutionError("<urllib3.connection.HTTPConnection object at 0x103eee750>: Failed to resolve 'themes' ([Errno 8] nodename nor servname provided, or not known)"))
2026-03-31 13:29:59,744 ERROR Error while requesting http://sites/default/files/css/css_9m8-tA3IQf8ThlLQYTTZUyEweCvyR908Tg0XCbKYOfY.css: HTTPConnectionPool(host='sites', port=80): Max retries exceeded with url: /default/files/css/css_9m8-tA3IQf8ThlLQYTTZUyEweCvyR908Tg0XCbKYOfY.css (Caused by NameResolutionError("<urllib3.connection.HTTPConnection object at 0x103efad10>: Failed to resolve 'sites' ([Errno 8] nodename nor servname provided, or not known)"))
2026-03-31 13:29:59,749 ERROR Error while requesting http://sites/default/files/css/css_WQ8gUsMawX4g-eNk2UuZlgR8odx0fG0fVctdPO75y5g.css: HTTPConnectionPool(host='sites', port=80): Max retries exceeded with url: /default/files/css/css_WQ8gUsMawX4g-eNk2UuZlgR8odx0fG0fVctdPO75y5g.css (Caused by NameResolutionError("<urllib3.connection.HTTPConnection object at 0x103f09fd0>: Failed to resolve 'sites' ([Errno 8] nodename nor servname provided, or not known)"))
2026-03-31 13:29:59,753 ERROR Error while requesting http://themes/spbgu/markup/dist/img/logo-big.svg: HTTPConnectionPool(host='themes', port=80): Max retries exceeded with url: /spbgu/markup/dist/img/logo-big.svg (Caused by NameResolutionError("<urllib3.connection.HTTPConnection object at 0x1029c3d10>: Failed to resolve 'themes' ([Errno 8] nodename nor servname provided, or not known)"))
2026-03-31 13:29:59,759 ERROR Error while requesting http://themes/spbgu/markup/dist/img/logo-text-smal.svg: HTTPConnectionPool(host='themes', port=80): Max retries exceeded with url: /spbgu/markup/dist/img/logo-text-smal.svg (Caused by NameResolutionError("<urllib3.connection.HTTPConnection object at 0x103e77f10>: Failed to resolve 'themes' ([Errno 8] nodename nor servname provided, or not known)"))
2026-03-31 13:29:59,762 ERROR Error while requesting http://themes/spbgu/sections_img/universitet.jpg: HTTPConnectionPool(host='themes', port=80): Max retries exceeded with url: /spbgu/sections_img/universitet.jpg (Caused by NameResolutionError("<urllib3.connection.HTTPConnection object at 0x103f11a50>: Failed to resolve 'themes' ([Errno 8] nodename nor servname provided, or not known)"))
2026-03-31 13:29:59,766 ERROR Error while requesting http://themes/spbgu/sections_img/education.jpg: HTTPConnectionPool(host='themes', port=80): Max retries exceeded with url: /spbgu/sections_img/education.jpg (Caused by NameResolutionError("<urllib3.connection.HTTPConnection object at 0x104504fd0>: Failed to resolve 'themes' ([Errno 8] nodename nor servname provided, or not known)"))
2026-03-31 13:29:59,776 ERROR Error while requesting http://themes/spbgu/sections_img/nauka.jpg: HTTPConnectionPool(host='themes', port=80): Max retries exceeded with url: /spbgu/sections_img/nauka.jpg (Caused by NameResolutionError("<urllib3.connection.HTTPConnection object at 0x103f131d0>: Failed to resolve 'themes' ([Errno 8] nodename nor servname provided, or not known)"))
2026-03-31 13:30:05,791 INFO URL: http://spbu.ru/prikol, Response Code: 404
```
скрин в браузере, на google.com работает чуть лучше, но тоже прикольно выглядит
<img width="1851" height="1329" alt="Screenshot 2026-03-31 at 13 31 26" src="https://github.com/user-attachments/assets/2c0c0fb2-7787-4394-80b0-91c52b962f26" />
<img width="2551" height="1301" alt="Screenshot 2026-03-31 at 13 32 45" src="https://github.com/user-attachments/assets/67f6b061-8a3c-4b4b-aa18-926531e79eb4" />

И POST:

Лог: `2026-03-31 13:38:36,378 INFO URL: http://httpbin.org/post, Response Code: 200`
<img width="1498" height="1119" alt="Screenshot 2026-03-31 at 13 39 07" src="https://github.com/user-attachments/assets/1a350508-1522-4acf-8d6f-621f909df94b" />


### Б. Прокси-сервер с кешированием (4 балла)
Когда прокси-сервер получает запрос, он проверяет, есть ли запрашиваемый объект в кэше, и,
если да, то возвращает объект из кэша без соединения с веб-сервером. Если объекта в кэше нет,
прокси-сервер извлекает его с веб-сервера обычным GET запросом, возвращает клиенту и
кэширует копию для будущих запросов.

Для проверки того, прокис объект в кеше или нет, необходимо использовать условный GET
запрос. В таком случае вам необходимо указывать в заголовке запроса значение для If-Modified-Since и If-None-Match. 
Подробности можно найти [тут](https://ruturajv.wordpress.com/2005/12/27/conditional-get-request).

Будем считать, что кеш-память прокси-сервера хранится на его жестком диске. Ваш прокси-сервер
должен уметь записывать ответы в кеш и извлекать данные из кеша (т.е. с диска) в случае
попадания в кэш при запросе. Для этого необходимо реализовать некоторую внутреннюю
структуру данных, чтобы отслеживать, какие объекты закешированы.

Приложите скрины или логи, из которых понятно, что ответ на повторный запрос был взят из кэша.

#### Демонстрация работы
Вроде сделал всё кроме max-age из ссылочки. Вернемся к истокам и постучимся на `http://gaia.cs.umass.edu/wireshark-labs/HTTP-wireshark-file2.html`
```
2026-03-31 14:00:00,875 INFO URL: http://gaia.cs.umass.edu/wireshark-labs/HTTP-wireshark-file2.html, Response Code: 200, Cache: MISS
2026-03-31 14:00:03,247 INFO URL: http://gaia.cs.umass.edu/wireshark-labs/HTTP-wireshark-file2.html, Response Code: 200, Cache: HIT
```
Ура!
Так же проверил после перезапуска сервера и всё верно считалось и опять попало в кэш.

### В. Черный список (2 балла)
Прокси-сервер отслеживает страницы и не пускает на те, которые попадают в черный список. Вместо
этого прокси-сервер отправляет предупреждение, что страница заблокирована. Список доменов
и/или URL-адресов для блокировки по черному списку задается в **конфигурационном файле**.

Приложите скрины или логи запроса из черного списка.

#### Демонстрация работы
Добавил это в прошлую реализацию, файл `proxy_b.py`

Вот такой лог `2026-03-31 14:08:04,799 INFO BLOCKED URL: http://google.com` и картинка:
<img width="1785" height="685" alt="Screenshot 2026-03-31 at 14 08 10" src="https://github.com/user-attachments/assets/dfe66514-8a03-43e5-b600-61673698f56e" />



## Wireshark. Работа с DNS
Для каждого задания в этой секции приложите скрин с подтверждением ваших ответов.

### А. Утилита nslookup (1 балл)

#### Вопросы
1. Выполните nslookup, чтобы получить IP-адрес какого-либо веб-сервера в Азии
   <img width="445" height="132" alt="Screenshot 2026-03-29 at 19 37 27" src="https://github.com/user-attachments/assets/df3f6345-421e-4eb7-8507-982ef6c7353c" />
   - Сайт Hong Kong Stock Exchange имеет два ip'шника 203.78.5.43 и 203.78.6.43
3. Выполните nslookup, чтобы определить авторитетные DNS-серверы для какого-либо университета в Европе
   - <img width="496" height="136" alt="Screenshot 2026-03-29 at 19 46 22" src="https://github.com/user-attachments/assets/30457589-a6f1-4f00-be8d-6d754bad191a" />
4. Используя nslookup, найдите веб-сервер, имеющий несколько IP-адресов. Сколько IP-адресов имеет веб-сервер вашего учебного заведения?
   - В первом задании уже нашел такое - сайт HKEX имеет два ip
   - У spbu один ip
   <img width="397" height="103" alt="Screenshot 2026-03-29 at 19 49 01" src="https://github.com/user-attachments/assets/2994a33b-e930-4bd0-969c-5580803e19c0" />


### Б. DNS-трассировка www.ietf.org (3 балла)

#### Подготовка
1. Используйте ipconfig для очистки кэша DNS на вашем компьютере.
2. Откройте браузер и очистите его кэш (для Chrome можете использовать сочетание клавиш
   CTRL+Shift+Del).
3. Запустите Wireshark и введите `ip.addr == ваш_IP_адрес` в строке фильтра, где значение
   ваш_IP_адрес вы можете получить, используя утилиту ipconfig. Данный фильтр позволит
   нам отбросить все пакеты, не относящиеся к вашему хосту. Запустите процесс захвата пакетов в Wireshark.
4. Зайдите на страницу www.ietf.org в браузере.
5. Остановите захват пакетов.

#### Вопросы
1. Найдите DNS-запрос и ответ на него. С использованием какого транспортного протокола
   они отправлены?
   - UDP
2. Какой порт назначения у запроса DNS?
   - 53
3. На какой IP-адрес отправлен DNS-запрос? Используйте ipconfig для определения IP-адреса
   вашего локального DNS-сервера. Одинаковы ли эти два адреса?
   - 192.168.0.1
   - Да, одинаковые
4. Проанализируйте сообщение-запрос DNS. Запись какого типа запрашивается? Содержатся
   ли в запросе какие-нибудь «ответы»?
   - Type A
   - Нет, только запрос
  
     <img width="1633" height="1197" alt="Screenshot 2026-03-29 at 22 26 06" src="https://github.com/user-attachments/assets/09cc85a2-a23a-43f9-a67d-49322dd85a0e" />
     (все ответы на прошлые вопросы с этого скрина видно)
5. Проанализируйте ответное сообщение DNS. Сколько в нем «ответов»? Что содержится в
   каждом?
   - 2 ответа
   - два ip'шника www.ietf.org: type A, class IN, addr 104.16.45.99 и www.ietf.org: type A, class IN, addr 104.16.44.99
 <img width="1633" height="1197" alt="Screenshot 2026-03-29 at 22 27 15" src="https://github.com/user-attachments/assets/09df918e-252f-41cb-b743-a7930c493bea" />
 
 А, ну и всякие подробности есть
<img width="512" height="173" alt="Screenshot 2026-03-29 at 22 29 05" src="https://github.com/user-attachments/assets/b0f779a2-2b55-41b8-9c55-b496a75761f5" />


6. Посмотрите на последующий TCP-пакет с флагом SYN, отправленный вашим компьютером.
   Соответствует ли IP-адрес назначения пакета с SYN одному из адресов, приведенных в
   ответном сообщении DNS?
   - есть такое. Соотвествует.
     <img width="1633" height="1197" alt="Screenshot 2026-03-29 at 22 36 50" src="https://github.com/user-attachments/assets/b6a1bb05-bdd5-44ab-b610-c85187f16416" />

7. Веб-страница содержит изображения. Выполняет ли хост новые запросы DNS перед
   загрузкой этих изображений?
   - Вроде нет
   Там конечно есть какие-то запросы до static.ietf.org и analytics.ietf.org, но они как-то далеко от первых запросов идут. И вроде это не то


### В. DNS-трассировка www.spbu.ru (2 балла)

#### Подготовка
1. Запустите захват пакетов с тем же фильтром `ip.addr == ваш_IP_адрес`
2. Выполните команду nslookup для сервера www.spbu.ru
3. Остановите захват
4. Вы увидите несколько пар запрос-ответ DNS. Найдите последнюю пару, все вопросы будут относиться к ней
   
#### Вопросы
1. Каков порт назначения в запросе DNS? Какой порт источника в DNS-ответе?
   - 53
   - 53
2. На какой IP-адрес отправлен DNS-запрос? Совпадает ли он с адресом локального DNS-сервера, установленного по умолчанию?
   - 192.168.0.1
   - да
3. Проанализируйте сообщение-запрос DNS. Запись какого типа запрашивается? Содержатся
   ли в запросе какие-нибудь «ответы»?
   - А
   - Нет
  <img width="1471" height="540" alt="Screenshot 2026-03-29 at 22 49 09" src="https://github.com/user-attachments/assets/2a854070-8ee1-46bf-978f-96d1a2b1269e" />

4. Проанализируйте ответное сообщение DNS. Сколько в нем «ответов»? Что содержится в каждом?
   - 1 ответ
   - ip 195.70.219.100 и всякая доп инфа
     <img width="1376" height="524" alt="Screenshot 2026-03-29 at 22 51 14" src="https://github.com/user-attachments/assets/975cf7e4-5093-4052-893f-836ee457b0f0" />


### Г. DNS-трассировка nslookup –type=NS (1 балл)
Повторите все шаги по предварительной подготовке из Задания B, но теперь для команды `nslookup –type=NS spbu.ru`

#### Вопросы
1. На какой IP-адрес отправлен DNS-запрос? Совпадает ли он с адресом локального DNS-сервера, установленного по умолчанию?
   - 192.168.0.1
   - да
  Всё также как и было до этого
2. Проанализируйте сообщение-запрос DNS. Запись какого типа запрашивается? Содержатся ли в запросе какие-нибудь «ответы»?
   - Typy NS
   - Нет
  <img width="1633" height="1197" alt="Screenshot 2026-03-29 at 23 12 47" src="https://github.com/user-attachments/assets/68757844-2fcc-4643-ae4c-1647b8e2543c" />

3. Проанализируйте ответное сообщение DNS. Имена каких DNS-серверов университета в
   нем содержатся? А есть ли их адреса в этом ответе?
   - ns.pu.ru, ns7.pu.ru, ns2.pu.ru
   - Есть, но только в части additional records
<img width="807" height="499" alt="Screenshot 2026-03-29 at 23 15 36" src="https://github.com/user-attachments/assets/16102477-47c8-431c-8b52-60fa678becbe" />

### Д. DNS-трассировка nslookup www.spbu.ru ns2.pu.ru (1 балл)
Снова повторите все шаги по предварительной подготовке из Задания B, но теперь для команды `nslookup www.spbu.ru ns2.pu.ru`.
Запись `nslookup host_name dns_server` означает, что запрос на разрешение доменного имени `host_name` пойдёт к `dns_server`.
Если параметр `dns_server` не задан, то запрос идёт к DNS-серверу по умолчанию (например, к локальному).

#### Вопросы
1. На какой IP-адрес отправлен DNS-запрос? Совпадает ли он с адресом локального DNS-сервера, установленного по умолчанию? 
   Если нет, то какому хосту он принадлежит?
   - Если смотреть до ns2.pu.ru то ответы будут такими же как и в прошлых заданиях - 192.168.0.1 и да
   - Если смотреть именно до spbu.ru, то там запрос идет на ip как раз этого ns2.pu.ru - 195.70.196.201 и нет
  
     <img width="1633" height="1197" alt="Screenshot 2026-03-29 at 23 38 02" src="https://github.com/user-attachments/assets/328bedcc-e36a-41fb-b605-19dc08327e4b" />

2. Проанализируйте сообщение-запрос DNS. Запись какого типа запрашивается? Содержатся
   ли в запросе какие-нибудь «ответы»?
   - Type A
   - нет
3. Проанализируйте ответное сообщение DNS. Сколько в нем «ответов»? Что содержится в
   каждом?
   - один
   - всё как обычно - ip и доп инфа
   - <img width="1633" height="1197" alt="Screenshot 2026-03-29 at 23 42 00" src="https://github.com/user-attachments/assets/2ed4868a-d77f-4ce7-b73a-f6484b048f9c" />


### Е. Сервисы whois (2 балла)
1. Что такое база данных whois?
   - распределённая база данных, в которой содержатся регистрационные данные владельцев доменных имен, ip-адресов и автономных систем
2. Используя различные сервисы whois в Интернете, получите имена любых двух DNS-серверов. 
   Какие сервисы вы при этом использовали?
   -  NS3-L2.NIC.RU и NS3.MOEX.COM
   - https://whois.ru/moex.com ну и кстати локально утилита хорошо показывает тоже
   <img width="1183" height="727" alt="Screenshot 2026-03-30 at 00 00 55" src="https://github.com/user-attachments/assets/041c4ee7-f5d6-451f-b28f-ae8f9b5dfbfb" />

4. Используйте команду nslookup на локальном хосте, чтобы послать запросы трем конкретным
   серверам DNS (по аналогии с Заданием Д): вашему локальному серверу DNS и двум DNS-серверам,
   найденным в предыдущей части.
   - <img width="512" height="303" alt="Screenshot 2026-03-30 at 00 04 01" src="https://github.com/user-attachments/assets/05310367-1b97-4984-bee8-5615f832bb55" />
