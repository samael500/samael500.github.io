Title: Загрузка видео на youtube
Date: 2015-08-22 18:00
Modified: 2015-08-22 18:00
Category: Python
Tags: python, youtube, oauth2, video upload
Image: /media/youtube-upload/youtube_logo.png
Summary:
    В одном из моих собственных проектов, возникла задача - автоматической
    загрузки видео на канал на `youtube`. Делается это достаточно просто, при
    помощи гугловского `api` клиента для `python`. Единственное затруднение
    вызвало полумагическое получение ключей доступа к `api`...
#

В одном из моих собственных проектов, возникла задача - автоматической
загрузки видео на канал на `youtube`. Делается это достаточно просто, при
помощи гугловского `api` клиента для `python`. Единственное затруднение
вызвало полумагическое получение ключей доступа к `api`.

##Авторизация

> Все коды доступа и ключи авторизации, использованные в статье, вымышленные.
> Любое совпадение с реально существующими или когда-либо существовавшими
> ключами случайно.

Для авторизации в сервисах google с помощью протокола
[oauth2](http://oauth.net/2/) необходимо зарегистрировать приложение и дать
ему соответсвующие права. Для этого нужно перейти в
[консоль разработчика](https://console.developers.google.com/project)

Нажимаем на кнопку `Create Project`, выбираем имя и создаем новое приложение.
После того как приложение будет создано, нужно добавить ему необходимые
доступы к google API.

![Create Project](/media/youtube-upload/create_proj.png){.shadow .center}

Для загрузки видео на `youtube` нужно добавить `YouTube Data API`.
Для этого переходим во вкладку `APIs & auth` &rarr; `APIs`.
Также во вкладке `APIs & auth` &rarr; `Credentials` нужно добавить доступы
для `oauth2` авторизации.

![Add Oauth2](/media/youtube-upload/oauth_cred.png){.shadow .center}

Указываем тип приложения `Other`.
Получаем доступы для авторизации: идентефикатор и пароль.

* Client ID `230452130504-3uca1rp4ntlh06hdnsdbj50sqagaqfkt.apps.googleusercontent.com`
* Client secret `qawsWCd3J6HTRvnqsjYUpgH9`

Получив данные для авторизации, нужно перейти по следующей ссылке, заменив в ней
параметр `client_id` на тот что Вы получили в предыдущем шаге.

```text
    https://accounts.google.com/o/oauth2/auth?
        client_id=230452130504-3uca1rp4ntlh06hdnsdbj50sqagaqfkt.apps.googleusercontent.com&
        redirect_uri=urn:ietf:wg:oauth:2.0:oob&
        scope=https://www.googleapis.com/auth/youtube&
        response_type=code&
        access_type=offline
```

Далее выбираем к какому аккаунту гугл будет иметь доступ приложение,
и соответсвенно к какому каналу на ютубе.

![account choice](/media/youtube-upload/account_choice.png){.shadow .center}

![ch choice](/media/youtube-upload/ch_choice.png){.shadow .center}

Соглашаемся с доступом к управлению каналом.

![access](/media/youtube-upload/access.png){.shadow .center}

Получаем токен авторизации следующего вида
`4/Rw6A9raJQ3PrPWL0Q9z49guYu89FZoz322RySVFtzNc`.

![code](/media/youtube-upload/code.png){.shadow .center}

После этого необходимо получить, так называемый, refresh_token, для этого нужно
отправить POST запрос c токеном авторизации по адресу
`https://accounts.google.com/o/oauth2/token`. Cделать это легко, при помощи
консольной утилиты curl.

```Bash
data=""\
"code=4/Rw6A9raJQ3PrPWL0Q9z49guYu89FZoz322RySVFtzNc&"\
"client_id=230452130504-3uca1rp4ntlh06hdnsdbj50sqagaqfkt.apps.googleusercontent.com&"\
"client_secret=qawsWCd3J6HTRvnqsjYUpgH9&"\
"redirect_uri=urn:ietf:wg:oauth:2.0:oob&"\
"grant_type=authorization_code"

curl --data $data "https://accounts.google.com/o/oauth2/token"
```

Токен авторизации сработает только один раз, при повторной попытке отправить
его будет получено `Code was already redeemed.`.
В ответ на корректный запрос, гугл возвращает json с временным токеном доступа
и постоянным обновляемым токеном (собственно он нам и нужен).

```json
{
    "access_token" : "ya29.1wGYJU7NP7Ul69c13aE1Vuvbx0LfxrsgMiBjXdNY3sU3tuE9LmuJ3nOGHeb3e_824LH0",
    "token_type" : "Bearer",
    "expires_in" : 3600,
    "refresh_token" : "1/g1ixyts83iMrtR71oFqwGp3LSGbHz6ByxsBThrHRWCNIgOrJDtdun6zK6XiATCKT"
}
```

Получив обновляемый токен, можем с его помощью каждый раз получать рабочий
токен доступа, который предоставляется временем на 3600 секунд.

```Bash
data=""\
"refresh_token=1/g1ixyts83iMrtR71oFqwGp3LSGbHz6ByxsBThrHRWCNIgOrJDtdun6zK6XiATCKT&"\
"client_id=230452130504-3uca1rp4ntlh06hdnsdbj50sqagaqfkt.apps.googleusercontent.com&"\
"client_secret=qawsWCd3J6HTRvnqsjYUpgH9&"\
"grant_type=refresh_token"

curl --data $data "https://accounts.google.com/o/oauth2/token"
```

В ответ гугл возвращает json с временным токеном доступа.

```json
{
  "access_token" : "ya29.2AHpPjacO0prQkip0svapohuZtoK0wqdh7u0ohH49l0WWwrSyss7CWiwzMy5wX967tWsjQ",
  "token_type" : "Bearer",
  "expires_in" : 3600
}
```

Получать этот токен доступа нужно будет каждые раз, при подключении к `api`.
Для этого напишем простую функицю на `python 3` с использованием стандартной
библиотеки `urllib.request`

```python

import json
import urllib
import urllib.request


def get_auth_code():
    """ Get access token for connect to youtube api """
    oauth_url = 'https://accounts.google.com/o/oauth2/token'
    # create post data
    data = dict(
        refresh_token=settings.YOUTUBE_REFRESH_TOKEN,
        client_id=settings.YOUTUBE_CLIENT_ID,
        client_secret=settings.YOUTUBE_CLIENT_SECRET,
        grant_type='refresh_token',
    )

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }

    data = urllib.parse.urlencode(data).encode('utf-8')
    # make request and take response
    request = urllib.request.Request(oauth_url, data=data, headers=headers)
    response = urllib.request.urlopen(request)

    # get access_token from response
    response = json.loads(response.read().decode('utf-8'))
    return response['access_token']

```

Вот теперь, мы наконец подошли к самой `oauth2` авторизации в сервисах гугл.
Для этого необходимо использовать следующие дополнительные библиотеки:

- [httplib2](https://pypi.python.org/pypi/httplib2)
- [oauth2client](https://pypi.python.org/pypi/oauth2client)
- [google-api-python-client](https://pypi.python.org/pypi/google-api-python-client)

Далее, используя выше описанную функцию получения временного токена, создаем
подключение к `youtube api`.

```python

import httplib2

from oauth2client.client import AccessTokenCredentials
from apiclient.discovery import build


def get_authenticated_service():
    """ Create youtube oauth2 connection """
    # make credentials with refresh_token auth
    credentials = AccessTokenCredentials(
        access_token=get_auth_code(), user_agent='my-awesome-project/1.0'
    )
    # create connection to youtube api
    return build(
        'youtube', 'v3', http=credentials.authorize(httplib2.Http())
    )

```

Теперь мы имеем созданное подключение, которое можно использовать для работы с `api`.

##Загрузка видео

...продолжение следует...
