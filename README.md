# Virtual wallet API
This API will allow you to manage you virtual wallet. This API is created on the base of Django REST framework.

## Installation
Repository can be clone from GitHub via command:

```github
git clone https://github.com/yurikoste/virtual_wallet_api.git
```
In order to build docker container you need installed [Docker Compose](https://docs.docker.com/compose/gettingstarted/) in your system.

Following commands are relevant for Linux systems:

```bash
cd <your_project_directory/>
```

```bash
sudo docker-compose build
```
After building of the container you have to run it with:
```bash
sudo docker-compose up
```

## Usage

You can access to the swagger by following link [http://0.0.0.0:8000/swagger/](http://0.0.0.0:8000/swagger/)

All endpoints are described in swagger and they have prefix http://0.0.0.0:8000/api/v1/ which you have to use if you would like to access API from the browser.



## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)

## References
[Virtual wallet API at GitHub.com](https://github.com/yurikoste/virtual_wallet_api)
