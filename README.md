# IntroLab Systems test
Web-scraper for <a href="https://finance.yahoo.com">finance.yahoo.com</a>
## Requirements
- docker-compose
## Usage
```shell
$ git clone https://github.com/quidow/IntroLab_Systems_test.git
$ cd ./IntroLab_Systems_test
$ chmod +x ./app/entrypoint.sh
$ docker-compose up --build --abort-on-container-exit
```
Files will be saved in "files" directory in the root of project.
