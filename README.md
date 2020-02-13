# AWS Hosted application deployment steps 
This will give a basic tutorial on how to install the elastic beanstalk CLI and deploy a dash app.



First install awsebcli with homebrew

```bash
$ brew install awsebcli
```

Then go here to learn how to set your path:
just follow step 3.

https://docs.amazonaws.cn/en_us/elasticbeanstalk/latest/dg/eb-cli3-install-linux.html

In your project directory run the following command and answer the prompts:

```bash
$ eb init 
```
The prompts are as follows
```bash
Select a default region
1) us-east-1 : US East (N. Virginia)
2) us-west-1 : US West (N. California)
3) us-west-2 : US West (Oregon)
4) eu-west-1 : EU (Ireland)
5) eu-central-1 : EU (Frankfurt)
6) ap-south-1 : Asia Pacific (Mumbai)
7) ap-southeast-1 : Asia Pacific (Singapore)
8) ap-southeast-2 : Asia Pacific (Sydney)
9) ap-northeast-1 : Asia Pacific (Tokyo)
10) ap-northeast-2 : Asia Pacific (Seoul)
11) sa-east-1 : South America (Sao Paulo)
12) cn-north-1 : China (Beijing)
13) cn-northwest-1 : China (Ningxia)
14) us-east-2 : US East (Ohio)
15) ca-central-1 : Canada (Central)
16) eu-west-2 : EU (London)
17) eu-west-3 : EU (Paris)
18) eu-north-1 : EU (Stockholm)
19) ap-east-1 : Asia Pacific (Hong Kong)
20) me-south-1 : Middle East (Bahrain)

(default is 3): 3
```
You can either then create a new app or initialize the project directory to an existing beanstalk app.

```bash
Select an application to use
1) testapp
2) LoadRunner Test Comparison Dash
3) [ Create new Application ]
(default is 3): 3

```

You then choose your platform from the following

```bash
Application test2 has been created.

Select a platform.
1) Node.js
2) PHP
3) Python
4) Ruby
5) Tomcat
6) IIS
7) Docker
8) Multi-container Docker
9) GlassFish
10) Go
11) Java
12) Packer
(default is 1): 3
```

The app should now exist on your elastic beanstalk on AWS. 
Congratulations.






