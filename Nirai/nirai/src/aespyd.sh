g++ -I/usr/include/python2.7 aes.cxx -lpython2.7 -lcrypto \
    -shared -fPIC -o aes.so -DBUILD_PYD -L/usr/local/opt/openssl/lib -I/usr/local/opt/openssl/include
