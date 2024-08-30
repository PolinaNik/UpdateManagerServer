# Update Manager для Astra Linux

Написано для встроенной версии python3.5

В этом репозитории находятся файлы для утилиты Update Manager. Утилита состоит из двух частей: серверная и клиентская.
На серверной части происходит:
- ввод основной информации;
- указание параметров для обновления;
- контроль над статусом обновления;
- хранение логов.

На клиентской части во время обновления в обычном режиме (не тихом) появляется окно с подтверждением. При согласии клиента происходит обновление, при отказе - окно исчезает и появляется вновь через 10 минут. Все действия клиента можно видеть в окне "статус обновлений" на серверной части.

## Серверная часть

Запуск производится при активации скрипта update_window.py. После запуска предполагается, что пользователь введет все необходимые данные:
- название версии (при пропуске заполнения этого поля - названием версии станет текущая дата);
- выберет рабочие места из списка (список корректируется в конфигурационном файле settings.ini);
- выберет режим. На выбор 2 режима: с подтверждением клиента и тихий. При выборе тихого режима появится уточняющее окно с подтверждением данного режима во избежание ошибок;
- выберет какой процесс нужно перезагрузить после обновления. На данный момент выбор процесса - это просто заглушка, ничего после обновления не происходит. Данную часть кода доработаю на месте;
- напишет комментарий. Текст комментария будет виден клиенту, когда появится окно с обновлением.

После того как все необходимые параметры введены, окно для ввода закроется и появится окно со статусом обновлений. В этом окне появится информация если:
- клиент обновился;
- клиент отложил обновление;
- нет доступа к клиенту

## Клиентская часть

Клиентская часть состоит из скрипта, который запускает окно во время обновления по сигналу с серверной части (если обновление не в тихом режиме).

## Что хочу доработать:
 - написать БД для хранения всех версий обновлений, чтобы наглядно было видно какая версия на каждом хосте в данный момент.
 - дописать код для отката, по сути все то же самое, только исходные данные для обновления будут из другой папки.

