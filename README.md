# rsa
A Python implementation of RSA encryption and decryption, as well as an algorithm for brute forcing a private key. Originally written for a university lab exercise.

##Usage

* Download all three modules into the same folder and import RSA into Python.
* Obtain a dictionary with key values n, d and e by calling RSA.chooseKeys().
* Obtain an encrypted hex string of a message M by calling RSA.encrypt(M, e, n).
* Obtain a decrypted message from a hex string H by calling RSA.decrypt(H, d, n).
* Obtain the private key (d, n) belonging to a public key (e, n) by calling crackPrivate(e, n).

Warning: Algorithms take a long time if key numbers are >16 bits.