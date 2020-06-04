# myurl
A simple url redirector based on python 3

## Deply via Docker

$ docker run -d -v /log/myurl:/log/ -p 8080:8080 linanw/myurl

## Usage

\<your domain or hostname\>:8080/\<any tag name\>?\<url to go with https:// or http://\>

e.g https://linanw.me/from_github?youtu.be/IT9c38lLEjc

## Log

In your /log/myurl/ folder your will see folders named by each tag you specified. Each file in the folders represent a access from your url. The file is named by the access date, time and the county the client is from. The file content are the request headers, request line and ip information.
