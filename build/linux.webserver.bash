# check apache is running
sudo systemctl is-enabled httpd

# start apache and ensure starts each time the system boots
sudo systemctl start httpd && sudo systemctl enable httpd

# enssure latest security updates and bug fixes
sudo yum update -y

# add TLS support by installing the Apache module mod_ssl.
sudo yum install -y mod_ssl
==> /etc/httpd/conf.d/ssl.conf
==> /etc/pki/tls/certs/make-dummy-cert

# run script to generate delf-signed dummay cerificate 
cd /etc/pki/tls/certs
sudo ./make-dummy-cert localhost.crt
==>  Matches SSLCertificateFile directive already in /etc/httpd/conf.d/ssl.conf

# open the ssl.conf file and comment out the 
sudo nano /etc/httpd/conf.d/ssl.conf

==> Comment Out existing 
==> #SSLCertificateKeyFile /etc/pki/tls/private/localhost.key

#restart apache
sudo systemctl restart httpd