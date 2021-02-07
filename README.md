Bruteforce Login
=================

A bruteforce script for login systems

Installation and Usage
----------------------

-   fork and clone the repository `https://github.com/`Your-User-Name`/bruteforce-login.git`
-   `pip3 install requirements.txt`
-   Run brute_force.py with the following parameters

| Parameter           | Shorts | Required         | Description                                     |
|---------------------|--------|------------------|-------------------------------------------------|
|  --url              |   -u   |      True        | bruteforce url                                  |
|  --headers-file     |   -hf  |      True        | The file consisting of all the required headers |
|---------------------|--------|------------------|-------------------------------------------------|
|  --password         |   -p   | One of -p or -pf | single password                                 |
|  --password-file    |   -pf  | is required      | path to passwords file                          |
|---------------------|--------|------------------|-------------------------------------------------|
|  --id               |   -i   | One of -i or     | single id                                       |
|  --id-file          |   -if  | -if is required  | path to ids file                                |
|---------------------|--------|------------------|-------------------------------------------------|
|  --is-present       |   -ip  | One of -ip or    | if present in response terminates the bruteforce|
|  --is-not-present   |  -inp  | -inp is required | value if not present in response terminates the bruteforce  |

### Example:
```
python3 brute_force.py -u https://.... -hf headers.txt -pf pass.txt -i adam -inp Invalid
``` 

Future Improvements:
--------------------
-   Resolve the issues due to rate limiters
-   Add a way to make custom payload for request
-   Add ways to accept payload type Example Formdata, json, ...etc
