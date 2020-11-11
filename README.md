A Fast API based python app for bed management.

Create a config.json with path configs/config.json with below structure

```
{
    "app_creds":{
        "username":"",
        "password":""
    }
}
```

Run the docker file with below command
```
sudo docker run -p 8000:8000 --name <continer_name> <image_name>
```
