# sslfreak
*Python script to check if a server accepts EXPORT ciphers based on https://gist.github.com/daybarr/987dddde385ec5e04af3
 
```
ssl_freak_check.py [-h] [--verbose] [--address ADDRESS] [--port PORT] [--ciphers CIPHERS]
```

```
python ssl_freak_check.py -a 'jabong.com' -c 'EXPORT'

Python: 2.7.8 (default, Oct 19 2014, 16:02:00) 
[GCC 4.2.1 Compatible Apple LLVM 6.0 (clang-600.0.54)]
OpenSSL: OpenSSL 1.0.2 22 Jan 2015
Expanding cipher list: EXPORT
3 ciphers found:
('EXP-DES-CBC-SHA', 'TLSv1/SSLv3', 40)
('EXP-RC2-CBC-MD5', 'TLSv1/SSLv3', 40)
('EXP-RC4-MD5', 'TLSv1/SSLv3', 40)
```
