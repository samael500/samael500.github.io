Title: Загрузка видео на youtube. Часть 1. Авторизация
Date: 2015-08-22 18:00
Modified: 2015-08-22 18:00
Category: Python
Tags: python, youtube, oauth2
Slug: youtube-upload-1
Image: /media/youtube-upload/youtube_logo.png
Summary:

#

Для авторизации в сервисах google с помощью протокола
[oauth2](http://oauth.net/2/) необходимо зарегистрировать приложение и дать
ему соответсвующие права. Для этого нужно перейти в
[консоль разработчика](https://console.developers.google.com/project)

Нажимаем на кнопку `Create Project`, выбираем имя и создаем новое приложение.
После того как приложение будет создано, нужно добавить ему необходимые
доступы к google API.

![Create Project](/media/youtube-upload/create_proj.png){.shadow}

Для загрузки видео на youtube нужно добавить `YouTube Data API`.
Для этого переходим во вкладку `APIs & auth` &rarr; `APIs`.
Также во вкладке `APIs & auth` &rarr; `Credentials` нужно добавить доступы
для `oauth2` авторизации.

![Add Oauth2](/media/youtube-upload/oauth_cred.png){.shadow}

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

###две картинки

Соглашаемся с доступом к управлению каналом.

###картинка

Получаем токен авторизации следующего вида
`4/Rw6A9raJQ3PrPWL0Q9z49guYu89FZoz322RySVFtzNc`.

###картинка

После этого необходимо получить, так называемый, refresh_token, для этого нужно
отправить POST запрос c токеном авторизации по адресу
`https://accounts.google.com/o/oauth2/token`. Cделать это легко, при помощи
коротенького скрипта на python-е.

```python
import urllib
import urllib.request


oauth_url = 'https://accounts.google.com/o/oauth2/token'

token = '4/IZuse1Q4RKMcFB4q3s8_01DnggJ0V9SUk8uMPEtIPW4'
client_id = '230452130504-3uca1rp4ntlh06hdnsdbj50sqagaqfkt.apps.googleusercontent.com'
client_secret = 'qawsWCd3J6HTRvnqsjYUpgH9'

# create post data
data = dict(
    code=token,
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri='urn:ietf:wg:oauth:2.0:oob',
    grant_type='authorization_code',
)

headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'application/json'
}

data = urllib.parse.urlencode(data).encode('utf-8')

# make request and take response
response = urllib.request.urlopen(
    urllib.request.Request(oauth_url, data=data, headers=headers)
)

print(response.read().decode('utf-8'))
```
Токен авторизации сработает только один раз, при повторной попытке отправить
его будет получено `HTTP Error 400: Bad Request`.
В ответ на корректный запрос, гугл возвращает json с временным токеном доступа
и постоянным обновляемым токеном (собственно он нам и нужен).

```json
{
  "access_token" : "ya29.1wFNkzdgo9uYdWAMQjuRXzpA7MWGzwN9mIeQLKL0oZk37yWpkSK_KA1Hd3Am85wmQgTr",
  "token_type" : "Bearer",
  "expires_in" : 3600,
  "refresh_token" : "1/NLUELtY7cZSQeBTbBIRYIUq4Ns55rwepPjWlcMvs9hY"
}
```