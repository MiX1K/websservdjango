sudo /etc/init.d/mysql start
mysql -uroot -e "create database likes_qa;"
mysql -uroot -e "grant all privileges on likes_qa.* to 'box'@'localhost' with grant option;"

