Aurora

See pricing: http://aws.amazon.com/rds/aurora/pricing/

2. Create an RDS DB Instance

   https://console.aws.amazon.com/rds/

   Select Amazon Aurora
     Choose instance sizes
     Multi-AZ deployment (No)
     Plublicly accessible (Yes)
     Specify db id, username, password (make a note of them)
     Select the same AZ where the private VPC was created
     Launch!

     Make a note of enpoint URL, ie:
     test.cluster-cu4nl3j4wvns.us-east-1.rds.amazonaws.com:3306


3. Create an EC2 instance

   https://console.aws.amazon.com/ec2/

   Choose Amazon Linux AMI - choose t2.micro
   Configure instance details
     Add storage (default)
     Tag instance (test-webserver)
     Configure Security Group - aurora-security-group
     Review and launch

     Create a new key pair - webserver-key-pair
     Download an SSH key

     Launch instances!

     While waiting look at: billing alerts

4. Connect to instance and install a webserver

   Download Putty: http://www.chiark.greenend.org.uk/~sgtatham/putty/
   Convert your PEM file

   Or connect using browser SSH connector plugin

   List EC2 instances, click on connect

   Copy ssh command and connect
   Note: you might need chmod 0600 key-pair.pem

   Install LAMP on the web server:
      sudo yum update -y
      sudo yum install -y httpd24 php56 php56-mysqlnd
      # Start webserver
      sudo service httpd start 
      # Automatically start on re-start
      sudo chkconfig httpd on
      chkconfig --list httpd

      Navigate to the public DNS (check address in EC2):
      ec2-51-22-164-178.compute-1.amazonaws.com

      # Secure the web server filesystem
      sudo groupadd www
      sudo usermod -a -G www ec2-user
      
      # reconnect to server
      exit
      ssh ....
      # verify groups were created
      groups

      # change files ownership
      sudo chown -R root:www /var/www
      sudo chmod 2775 /var/www
      find /var/www -type d -exec sudo chmod 2775 {} +
      find /var/www -type f -exec sudo chmod 0664 {} +

  Connect to RDS Aurora

      cd /var/www
      mkdir inc
      cd inc
      nano dbinfo.inc

      Use following:

<?php

define('DB_SERVER', 'endpoint');
define('DB_USERNAME', 'tutorial_user');
define('DB_PASSWORD', 'master password');
define('DB_DATABASE', 'sample');

?>

    cd /var/www/html
    nano SamplePage.php

    copy/paste SamplePage.php from github aurora/SamplePage.php

    Navigate to your page:
    http://ec2-52-23-169-179.compute-1.amazonaws.com/SamplePage.php

  Manually connect to your Aurora cluster:

    sudo yum install mysql
    mysql -u tutorial_user -p --host endpoint sample

  Assign Elastic IP

    https://console.aws.amazon.com/ec2/v2/home?region=us-east-1#Addresses:sort=publicIp

    


