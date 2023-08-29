# OperatorControl
Программа для контроля присутствия на рабочем месте оператора видеонаблюдения.
Принцип действия: 

После запуска Main.py на экране появится окно логина

![image](https://github-production-user-asset-6210df.s3.amazonaws.com/51487497/263969409-62f7c082-3cd1-4794-a9d3-8dff1e067e24.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWNJYAX4CSVEH53A%2F20230829%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20230829T092901Z&X-Amz-Expires=300&X-Amz-Signature=51ec66e5eccfc41454396139d25a7a09355c829945a686847777fe01e077541b&X-Amz-SignedHeaders=host&actor_id=51487497&key_id=0&repo_id=377568696)

Если пользователь заходит под учетной записью admin, то открывается окно настроек:

![image](https://github-production-user-asset-6210df.s3.amazonaws.com/51487497/263968215-b7c9df70-ac5b-480d-a8cb-4702966110d1.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWNJYAX4CSVEH53A%2F20230829%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20230829T092647Z&X-Amz-Expires=300&X-Amz-Signature=094d5908c229c0e051d31be9a6a9e628954a9538d4f2af01a273db3095c1f747&X-Amz-SignedHeaders=host&actor_id=51487497&key_id=0&repo_id=377568696)


Если выполнен вход под одной из учетных записей операторов, то блокируется нажатие большинства кнопок клавиатуры, а на всех мониторах отображаются полноэкранные прозрачные окна, предотвращающие случайные нажатия мышкой оператором.

С периодичностью, указанной в настройках, на экране появляется контрольное окно вида:

![image](https://github-production-user-asset-6210df.s3.amazonaws.com/51487497/263971583-ce5532eb-7d9c-4555-a53b-07737330b7b4.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWNJYAX4CSVEH53A%2F20230829%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20230829T093632Z&X-Amz-Expires=300&X-Amz-Signature=620dc59313ef8cc318c7cbd0b8200301a0ef4c88f145ec81556c2e0dfd41f443&X-Amz-SignedHeaders=host&actor_id=51487497&key_id=0&repo_id=377568696)


Нажатие/отсутствие нажатия кнопок за отведенный период фиксируется в текстовом файле, который отправляется на указанную в настройках почту по окончании смены оператора

Контрольный код был введен на случай, когда у оператора отсутствуют элементы управления ПК, для письменной фиксации кода

Пароль admin по-умолчанию: admin