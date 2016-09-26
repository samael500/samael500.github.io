Title: Отчеты coverage в TeamCity
Date: 2016-09-26 15:00
Modified: 2016-09-26 15:00
Category: Другое
Tags: ci, coverage, python, github, teamcity
Image: /media/teamcity-coverage/banner.png
Summary:
    Мы, в [WB--Tech](http://wbtech.pro/) в качестве системы неприрывной
    интеграции используем [TeamCity](https://www.jetbrains.com/teamcity/).
    А саму разработку ведем в приватных репозиториях
    на [github](https://github.com/). С задачей запуска тестов и публикации
    статуса выполнения вветку на `github` `TeamCity` справляется отлично. Но
    выводить отчет по покрытию кода
    [изкоробки](https://confluence.jetbrains.com/display/TCD9/Code+Coverage)
    умеет только для `Java` и `.NET`, а это не наш профиль.
    Хотелось получить собственную систему, похожую на
    [Coveralls](https://coveralls.io/github/Samael500) работающую с `python`.

Мы, в [WB--Tech](http://wbtech.pro/) в качестве системы неприрывной
интеграции используем [TeamCity](https://www.jetbrains.com/teamcity/).
А саму разработку ведем в приватных репозиториях
на [github](https://github.com/). С задачей запуска тестов и публикации
статуса выполнения вветку на `github` `TeamCity` справляется отлично. Но
выводить отчет по покрытию кода
[изкоробки](https://confluence.jetbrains.com/display/TCD9/Code+Coverage)
умеет только для `Java` и `.NET`, а это не наш профиль.
Хотелось получить собственную систему, похожую на
[Coveralls](https://coveralls.io/github/Samael500) работающую с `python`.

В результате статус пулреквеста зависит от проверки покрытия кода.

![pending](/media/teamcity-coverage/github_pending.png){.center}

![failure](/media/teamcity-coverage/github_failure.png){.center}

![success](/media/teamcity-coverage/github_success.png){.center}

## Формирование отчета

Первым делом, необходимо сформировать данные о покрытии кода. Делаем это
с помощью утилиты [Coverage.py](https://coverage.readthedocs.io/).
Т.к. для удобства работы с проектом, мы используем `Makefile`,
то пропишем в нем дополнительные команды, для запуска тестов с покрытием кода,
и формирования отчета.


```Makefile
VENV_PATH := $(HOME)/venv/bin
PROJ_NAME := my_awesome_project

# ...

ci_test: cover_test cover_report

cover_test:
    $(VENV_PATH)/coverage run --source=$(PROJ_NAME) manage.py test -v 2 --noinput

cover_report:
    $(VENV_PATH)/coverage report -m
    $(VENV_PATH)/coverage html
    $(VENV_PATH)/coverage-badge > htmlcov/coverage.svg
```

Команда `cover_test` запускает джанговские тесты, и замеряет покрытие кода.
Команда `cover_report` выводит в консоль отчет о покрытии, а так же формирует
`html` отчет и, при помощи утилиты
[coverage-badge](https://github.com/dbrgn/coverage-badge) формирует красивый
беджик со статусом покрытия кода ![badge](/media/teamcity-coverage/badge.svg).

После того, как исходные данные для отчета подготовлены, мы можем отображать
результат. Для этого нужно сконфигугрировать сбор артифактов в `teamcity`.
Делается это на вкладке `General Settings` в настройках проекта. Мы копируем в
артифакты папку `htmlcov` содержащую отчет и беджик.

![General Settings](/media/teamcity-coverage/artifacts.png){.center .shadow}

После следующего запуска тестов, перейдя во вкладку `Artifacts`, можно увидеть
дерево артифактов данного билда.

![Artifacts tree](/media/teamcity-coverage/artifacts_tree.png){.center .shadow}

Сами артифакты так же доступны авторизованым пользователям `TeamCity`
напрямую по ссылкам вида:

- `/repository/download/%teamcity.project.id%/%teamcity.build.id%:id/htmlcov/index.html`
- `/repository/download/%teamcity.project.id%/.lastFinished/htmlcov/index.html`

Более подробно о доступе к артифактам в [документации](https://confluence.jetbrains.com/display/TCD9/Patterns+For+Accessing+Build+Artifacts).

## Уведомления статуса на Github

Имея готовый отчет будем отправлять вебхуки на `github` с указаним статуса
покрытия кода. Для этого добавим простые `build steps`.

![Build steps](/media/teamcity-coverage/build_steps.png){.center .shadow}

#### Coverage pending hook

Заставляем гитхаб ждать отчета по покрытию кода.

- **Runner type** _Command Line_
- **Execute step** _Even if some of the previous steps failed_

**Custom script**
```bash
OWNER="<GITHUB OWNER>";
REPO="<REPO NAME>";
SHA="%build.vcs.number%";

curl "https://api.github.com/repos/$OWNER/$REPO/statuses/$SHA" \
    -X POST \
    -H "Content-Type: application/json" \
    -H "Authorization: token <GITHUB API TOKEN>" \
    -d '{
        "state": "pending",
        "description": "Coverage pending.",
        "context": "continuous-integration/coverage"
    }'
```

#### Badge copy

Копируем сформированный беджик, в папку доступную напрямую через вебсервер.
Для того, что бы `github` имел доступ к беджику без аутентификации в `teamcity`.
Если у вас разрешен гостевой доступ - то этот шаг выполнять не обязательно.

- **Runner type** _Command Line_
- **Execute step** _Even if some of the previous steps failed_

**Custom script**
```bash
BADGE="/path/to/public/dir/badges/%teamcity.project.id%/%teamcity.build.branch%-coverage.svg"
DIR=$(dirname "${BADGE}")
mkdir -p $DIR
cp -f htmlcov/coverage.svg $BADGE
```

#### Coverage finish hook

По окончанию тестов, отправляем отчет на гитхаб.

- **Runner type** _Command Line_
- **Execute step** _Even if some of the previous steps failed_

**Custom script**
```bash
OWNER="<GITHUB OWNER>";
REPO="<REPO NAME>";
SHA="%build.vcs.number%";

REPORT_URL="http://<YOU TEAMCITY DOMAIN>/repository/download/%teamcity.project.id%/%teamcity.build.id%:id/htmlcov/index.html";

COVERAGE=$(cat ./htmlcov/index.html | grep '<span class="pc_cov">' | grep -o '[0-9]\+');

if [ "$COVERAGE" -ge "85" ]; then
    STATUS='success';
else
    STATUS='failure';
fi

curl "https://api.github.com/repos/$OWNER/$REPO/statuses/$SHA" \
    -X POST \
    -H "Content-Type: application/json" \
    -H "Authorization: token <GITHUB API TOKEN>" \
    -d '{
        "state": "'$STATUS'",
        "target_url": "'$REPORT_URL'",
        "description": "Coverage '$COVERAGE'%",
        "context": "continuous-integration/coverage"
    }'
```

В данном случае, если покрытие менее 85%, то данная проверка будет считаться
ошибкой, и в гитхабе отметиться красным крестиком.

![fail](/media/teamcity-coverage/coverage_fail.png){.center .shadow}

![success](/media/teamcity-coverage/coverage_success.png){.center .shadow}

#### Беджик в readme

Для отображения беджика в `README.md` добавим ссылку, на последний успешний билд.

```shell
[![coverage report](http://<TEAMCITY DOMAIN>/badges/<TEAMCITY PROJ ID>/master-coverage.svg)](http://<TEAMCITY DOMAIN>/repository/download/<TEAMCITY PROJ ID>/.lastFinished/htmlcov/index.html)
```

Где `/badges/<TEAMCITY PROJ ID>/` доступна для анонимных посетиелей, что бы `github` мог закешировать изображение.

Теперь в `README` виден кликабельный беджик с покрытием кода.

![readme](/media/teamcity-coverage/readme.md.png){.center .shadow}

Кликнув на который, мы попадаем в отчет по покрытию кода.

![report](/media/teamcity-coverage/report.png){.center .shadow}
