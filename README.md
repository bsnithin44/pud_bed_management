A Fast API based python app for bed management.

Create my_secrets.py at below content

```
username = '<username>'
password = '<passowrd>'
```

Run the docker file with below command
```
sudo docker run -p 8000:8000 --name pud_test_deploy <image_name>
```