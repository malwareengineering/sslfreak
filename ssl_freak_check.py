#!/usr/bin/env python
import argparse
import logging
import socket
import ssl
import sys

def parse_args(argv):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Turn on debug logging")
    parser.add_argument("--address", "-a",
                        default='google.com',
                        help="Website adrres/ip")
    parser.add_argument("--port", "-p",
                        default= 443,
                        help="SSL port")
    parser.add_argument("--ciphers", "-c",
                        default=ssl._DEFAULT_CIPHERS,
                        help="Cipher list to test. Defaults to this python's "
                        "default client list")
    args = parser.parse_args(argv[1:])
    return args

if __name__ == "__main__":
    args = parse_args(sys.argv)

    log_level = logging.DEBUG if args.verbose else logging.INFO

    logging.basicConfig(level=log_level)
    logger = logging.getLogger("client")

    chosen_ciphers = []
    try:
        cipher_list = args.ciphers
        server_addr = (args.address, args.port)
        while True:
            client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_sock = ssl.wrap_socket(client_sock,
                                          ssl_version=ssl.PROTOCOL_SSLv23,
                                          ciphers=cipher_list)
            logger.debug("Connecting to %r", server_addr)
            client_sock.connect(server_addr)
            logger.debug("Connected")

            chosen_cipher = client_sock.cipher()
            chosen_ciphers.append(chosen_cipher)

            client_sock.write("ping")
            client_sock.close()

            # Exclude the first choice cipher from the list, to see what we get
            # next time.
            cipher_list += ':!' + chosen_cipher[0]
    except ssl.SSLError as err:
        if 'handshake failure' in str(err):
            logger.debug("Handshake failed - no more ciphers to try")
        else:
            logger.exception("Something bad happened")
    except Exception:
        logger.exception("Something bad happened")

    print("Python: {}".format(sys.version))
    print("OpenSSL: {}".format(ssl.OPENSSL_VERSION))
    print("Expanding cipher list: {}".format(args.ciphers))
    print("{} ciphers found:".format(len(chosen_ciphers)))
    print("\n".join(repr(cipher) for cipher in chosen_ciphers))
