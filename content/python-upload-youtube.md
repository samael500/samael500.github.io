Title: Загрузка видео на youtube
Date: 2015-08-22 18:00
Modified: 2015-08-26 18:00
Category: Python
Tags: python, youtube, oauth2, video upload
Image: /media/youtube-upload/python_youtube.jpg
Summary:
    В одном из моих собственных проектов, возникла задача автоматической
    загрузки видео на канал на `youtube`. Делается это достаточно просто, при
    помощи гугловского `api` клиента для `python`. Единственное затруднение
    вызвало полумагическое получение ключей доступа к `api`...
#

В одном из моих собственных проектов, возникла задача автоматической
загрузки видео на канал на `youtube`. Делается это достаточно просто, при
помощи гугловского `api` клиента для `python`. Единственное затруднение
вызвало полумагическое получение ключей доступа к `api`.

##Авторизация

> Все коды доступа и ключи авторизации, использованные в статье, вымышленные.<br />
> Любое совпадение с реально существующими или когда-либо существовавшими
> ключами случайно.

Для авторизации в сервисах `google` с помощью протокола
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
Получаем доступы для авторизации: идентификатор и пароль.

* Client ID `230452130504-3uca1rp4ntlh06hdnsdbj50sqagaqfkt.apps.googleusercontent.com`
* Client secret `qawsWCd3J6HTRvnqsjYUpgH9`

Получив данные для авторизации, нужно перейти по следующей ссылке, заменив в ней
параметр `client_id` на тот, что Вы получили в предыдущем шаге.

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

После этого необходимо получить, так называемый, `refresh_token`, для этого нужно
отправить `POST` запрос с токеном авторизации по адресу
`https://accounts.google.com/o/oauth2/token`. Сделать это легко, при помощи
консольной утилиты [curl](http://curl.haxx.se/).

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
В ответ на корректный запрос, гугл возвращает `json` с временным токеном доступа
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

В ответ гугл возвращает `json` с временным токеном доступа.

```json
{
  "access_token" : "ya29.2AHpPjacO0prQkip0svapohuZtoK0wqdh7u0ohH49l0WWwrSyss7CWiwzMy5wX967tWsjQ",
  "token_type" : "Bearer",
  "expires_in" : 3600
}
```

Получать этот токен доступа нужно будет каждые раз, при подключении к `api`.
Для этого напишем простую функцию на `python 3` с использованием стандартной
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

Вообще в руководстве по работе с `youtube api` рекомендуют использовать построение
`oauth2` подключения с использованием объекта `flow_from_clientsecrets`,
[примерно так](https://developers.google.com/youtube/v3/guides/uploading_a_video):

```python
def get_authenticated_service(args):
    flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
        scope=YOUTUBE_UPLOAD_SCOPE,
        message=MISSING_CLIENT_SECRETS_MESSAGE)

    storage = Storage("%s-oauth2.json" % sys.argv[0])
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        credentials = run_flow(flow, storage, args)

    return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
        http=credentials.authorize(httplib2.Http()))
```

Но, как выяснилось на практике, такой подход, требует при каждой загрузки,
давать разрешение на подключение к аккаунту `youtube` вручную,
это не очень удобно. Учитывая, что можно замечательным образом получать
токен авторизации, из обновляемого токена, мы будем использовать для создания
`oauth2` подключения - объект `AccessTokenCredentials`.

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

Теперь мы имеем созданное подключение,
которое можно использовать для работы с `api`.

##Загрузка видео

Имея готовое подключение к `api` загрузка видео происходит элементарно.

Определим функцию инициализации загрузки, которая принимает в качестве
аргументов подключение к `youtube api` и объект с информацией о видео.

```python
from apiclient.http import MediaFileUpload


def initialize_upload(youtube, card):
    """ Create youtube upload data """
    # create video meta data
    body = card.youtube_meta_data()
    # Call the API's videos.insert method to create and upload the video
    insert_request = youtube.videos().insert(
        part=",".join(body.keys()), body=body,
        media_body=MediaFileUpload(card.video.path, chunksize=-1, resumable=True))
    # wait for file uploading
    return resumable_upload(insert_request)
```

Метод `youtube_meta_data` должен возвращать словарь описания видео согласно
[формату](https://developers.google.com/youtube/v3/docs/videos), например:

```python
{
    "snippet": {
        "title": "Summer vacation in California",
        "description": "Had fun surfing in Santa Cruz",
        "tags": ["surfing", "Santa Cruz"],
        "categoryId": "22"
    },
    "status": {
        "privacyStatus": "private"
    }
}
```

В моем случае данный метод имел следующий вид:
```python

    def youtube_meta_data(self):
        """ Create metadata dict for youtube video upload """
        return dict(
            snippet=dict(
                title=settings.YOUTUBE_TITLE.format(coord=self.position),
                tags=settings.YOUTUBE_TAGS,
                categoryId=settings.YOUTUBE_CATEGORY_ID,
                description='{desc}\n{site_url}/{card_id}'.format(
                    desc=self.description, site_url=settings.SITE_URL, card_id=self.get_absolute_url()),
            ),
            status=dict(
                privacyStatus=settings.YOUTUBE_PRIVACY_STATUS,
            ),
            recordingDetails=dict(
                location=dict(
                    latitude=str(self.position.latitude),
                    longitude=str(self.position.longitude),
                ),
            ),
        )
```

После инициализации загрузки, необходимо поддерживать соединение и дождаться
ответа от ютуба с идентификатором видео. Для этого будем использовать
следующую функцию.

```python
import random
import http
import httplib2

# Explicitly tell the underlying HTTP transport library not to retry, since we are handling retry logic ourselves.
httplib2.RETRIES = 1

# Maximum number of times to retry before giving up.
MAX_RETRIES = 10

# Always retry when these exceptions are raised.
RETRIABLE_EXCEPTIONS = (
    httplib2.HttpLib2Error, IOError, http.client.NotConnected,
    http.client.IncompleteRead, http.client.ImproperConnectionState,
    http.client.CannotSendRequest, http.client.CannotSendHeader,
    http.client.ResponseNotReady, http.client.BadStatusLine)

# Always retry when an apiclient.errors.HttpError with one of these status codes is raised.
RETRIABLE_STATUS_CODES = (500, 502, 503, 504)


def resumable_upload(insert_request):
    response = None
    error = None
    retry = 0
    while response is None:
        try:
            status, response = insert_request.next_chunk()
            if 'id' in response:
                return response['id']
        except HttpError as err:
            if err.resp.status in RETRIABLE_STATUS_CODES:
                error = True
            else:
                raise
        except RETRIABLE_EXCEPTIONS:
            error = True

        if error:
            retry += 1
            if retry > MAX_RETRIES:
                raise Exception('Maximum retry are fail')

            sleep_seconds = random.random() * 2 ** retry
            time.sleep(sleep_seconds)
```

Таким образом, загрузка видео запускается функцией `initialize_upload`:

```python
video_id = initialize_upload(get_authenticated_service(), card)
```

Полный код загрузки видео можно посмотреть в
[gist](https://gist.github.com/Samael500/ac6eb61b11a7c3751753).

##Санкции

