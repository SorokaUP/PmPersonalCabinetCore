# Личный кабинет для запроса информации о статусах КИЗ в системе МДЛП (ядро)

Работает в связке с проектом [PmPersonalCabinet](https://github.com/SorokaUP/PmPersonalCabinet)

---

Проект обрабатывает запросы к RestApi МДЛП (метод запроса статусов КИЗ), полученные данные передает внешним программам. 
Отправка данных осуществляется посредством подписи с помощью УКЭП через собственную библиотеку Windows на C# (CryptApi.dll), 
которая по отпечатку публичного ключа получает из реестра сертификат и производит подпись сообщения.

---

В проекте использованы:
* Внешняя библиотека Windows собственной разработки для работы с УКЭП (CryptApi.dll) из реестра Windows.
