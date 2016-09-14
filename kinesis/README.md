Kinesis


## Kinesis agent

See for more info: http://docs.aws.amazon.com/firehose/latest/dev/writing-with-agents.html#setting-up-agent

### Installation 

```
sudo yum install –y aws-kinesis-agent
```

### Configuration

Task: Create IAM user, give him access to Kinesis Firehose, CloudWatch. Or reuse existing user.

Edit: `sudo nano /etc/sysconfig/aws-kinesis-agent`
And the S3 key and secret key.
```
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_DEFAULT_REGION=us-east-1
```

Setup new Kinesis Firehose:
https://console.aws.amazon.com/firehose/

Create new Delivery Stream: destination S3, test-kinesis1, logs- prefix
Use 1MB and 60s
Make sure IAM role has access to S3.

Make sure we store access logs in Apache webserver (this step might not be necessary if the log already exists):
```
sudo nano /etc/httpd/conf.d/welcome.conf
# add: 
CustomLog /var/log/httpd/access_log combined
# Restart Apache webserver
sudo service httpd restart
```

Visit sample welcome page and make sure logs are generated:
```
sudo tailf /var/log/httpd/access_log
```

Edit Kinesis Agent configuration: 
```
sudo nano /etc/aws-kinesis/agent.json
```

Example configuration:
```
{ 
    "flows": [
        {
            "filePattern": "/var/log/httpd/access_log", 
            "deliveryStream": "test-kinesis1"
        }
    ] 
}
```

Make sure Kinesis agent has read access:
```
sudo chmod -R go+rX /var/log/httpd
```

Start agent:
```
sudo service aws-kinesis-agent start
# To ensure it starts automatically after server restart
sudo chkconfig aws-kinesis-agent on
```

Check if there are any errors:
```
less /var/log/aws-kinesis-agent/aws-kinesis-agent.log
```

Generate more records:
```
ab -n 10000 -c 10 -k -H "Accept-Encoding: gzip, deflate" http://ec2-ip-address.compute-1.amazonaws.com/
```

Check if logs appear in S3.
