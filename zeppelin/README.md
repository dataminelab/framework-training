
# Zeppelin Tutorial

Run local Zeppelin:

```
docker run --rm --name zeppelin -p 8080:8080 dylanmei/zeppelin
```

See:
https://hub.docker.com/r/dylanmei/zeppelin/

Visit: 
http://localhost:8888/

* Navigate to: http://localhost:8080/
* Open tutorial notebook - basic features

Follow these steps:
* Enter bash in the container
```
docker exec -it zeppelin /bin/bash
wget -O hamlet.txt https://ia802607.us.archive.org/13/items/shakespeareshaml01shak/shakespeareshaml01shak_djvu.txt
```
* Create new notebook
* Run the following scala examples

```
# Start with something easy - word-count
val file = sc.textFile("file:////usr/zeppelin/hamlet.txt")
```

Follow the examples from here:
https://github.com/dataminelab/framework-training/blob/master/spark/spark.txt

Tutorial based on:
* Zeppelin docker
* https://zeppelin.apache.org/docs/0.5.5-incubating/tutorial/tutorial.html

* Real time streaming (old code)

https://apps.twitter.com/
Follow steps from: https://zeppelin.apache.org/docs/0.5.5-incubating/tutorial/tutorial.html

