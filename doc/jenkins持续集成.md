#服务器
    47.96.99.68 root A111.

##cd mnt 

##yum install java 

##安装tomcat
        
        wget http://mirror.bit.edu.cn/apache/tomcat/tomcat-10/v10.0.0-M1/bin/apache-tomcat-10.0.0-M1.zip
        
##安装maven(yum install maven)
        
        wget http://mirrors.tuna.tsinghua.edu.cn/apache/maven/maven-3/3.6.3/binaries/apache-maven-3.6.3-bin.zip

##yum install git 

        git config --global user.name "sa.wang"
        git config --global user.email  "513969457@qq.com"
        cd ~/.ssh
        ls
        //看是否存在 id_rsa 和 id_rsa.pub文件，如果存在，说明已经有SSH Key
        ssh-keygen -t rsa -C "513969457@qq.com"
        cat id_rsa.pub
        //拷贝秘钥 ssh-rsa开头
        ssh -T git@github.com
        //运行结果出现类似如下
        Hi WSG88! You've successfully authenticated, but GitHub does not provide shell access.
