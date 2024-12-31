# murus
production-ready middleware for flask with common security and performance features

murus (*latin: wall*) is an efficient package that offers JWT creation authentication, rate limiting, mutual TLS, security headers, and more with a minimal boilerplate / plug-and-play setup for APIs or sub-million (or perhaps more) scale apps.
it contains some relatively smart defaults alongside ergonomic shorthands and decorator functions that allow for a dynamic and efficient security and performance boost to WSGI deployments.

should be installable with `git+...` with `pip` and has a showcase app in `examples/`. the vision is to focus on development of core features and have `murus` handle most attack vectors. 
