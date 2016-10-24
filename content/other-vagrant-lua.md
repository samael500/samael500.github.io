Title: xxx
Date: 2016-10-25 15:00
Modified: 2016-10-25 15:00
Category: Другое
Tags: vagrant, lua, nginx, self-hosted, best
Image: /media/teamcity-coverage/banner.png
Image_width: 735
Image_height: 455
Summary:
    Для удобной разработки, быстрого переключения между проектами и
    эффективного взаимодействия бэкенд и фронтенд комманд. Мы, в
    [WB--Tech](http://wbtech.pro/) ведем разработку в виртуальном окружении
    [Vagrant](https://www.vagrantup.com/) + [VirtualBox](https://www.virtualbox.org/).
    `Vagrant` -- прекрасный менеджер окружения, а для ускорения развертывания
    виртуальной машины можно использовать компилированные, версированные боксы.
    Хостить их можно на [родном сервере](https://atlas.hashicorp.com/boxes/search),
    но в таком случае необходим либо смириться с публичным поиском, либо
    использовать `enterprise`. Триал у нас закончился, всязи с чем было решено
    хостить боксы на своем сервере. А сделали мы это с помощью [lua](https://www.lua.org/).

Для удобной разработки, быстрого переключения между проектами и
эффективного взаимодействия бэкенд и фронтенд комманд. Мы, в
[WB--Tech](http://wbtech.pro/) ведем разработку в виртуальном окружении
[Vagrant](https://www.vagrantup.com/) + [VirtualBox](https://www.virtualbox.org/).
`Vagrant` -- прекрасный менеджер окружения, а для ускорения развертывания
виртуальной машины можно использовать компилированные, версированные боксы.
Хостить их можно на [родном сервере](https://atlas.hashicorp.com/boxes/search),
но в таком случае необходим либо смириться с публичным поиском, либо
использовать `enterprise`. Триал у нас закончился, всязи с чем было решено
хостить боксы на своем сервере. А сделали мы это с помощью [lua](https://www.lua.org/).

Версийность боксов в `Vagrant` описывается при помощи `json`
[документа](https://www.vagrantup.com/docs/boxes/format.html).

```json
{
  "name": "hashicorp/precise64",
  "description": "This box contains Ubuntu 12.04 LTS 64-bit.",
  "versions": [
    {
      "version": "0.1.0",
      "providers": [
        {
          "name": "virtualbox",
          "url": "http://somewhere.com/precise64_010_virtualbox.box",
          "checksum_type": "sha1",
          "checksum": "foo"
        }
      ]
    }
  ]
}
```
