# Iron Hello World

## Setup


### install rust
```$ curl -sSf https://static.rust-lang.org/rustup.sh | sh```

### build project
```$ cargo build```

#### Mac errors & fixes in setup:
`fatal error: 'openssl/ssl.h' file not found`.
```
export OPENSSL_INCLUDE_DIR=/usr/local/opt/openssl/include
export DEP_OPENSSL_INCLUDE=/usr/local/opt/openssl/include
```

`note: ld: library not found for -lssl`
https://github.com/sfackler/rust-openssl

### run project
```
$ cargo run
```
