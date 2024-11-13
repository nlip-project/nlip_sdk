# NLIP SDK

The NLIP SDK provides the basic functionality that is needed to implement the NLIP protocol, either on the client side or on the server side. The server side requires additional packages. The NLIP SDK is targeted primarily at NLIP clients. 

The NLIP SDK contains the following modules: 

* utils.py - A set of basic utility routines that simplify implementation. 
* errrors.py - A set of error definitions that help diagnose in development. 
* nlip.proto - The protocol buffer formated messages for NLIP protocol
* nlip_pb2.py - Compiled proptol buffer messages. 
* nlip.py - The definition of the NLIP methods. 

#Generating Python Code from .proto File

## Publishing the Package

To publish the package to PyPI, ensure that your changes are committed and then create a version tag. You can do this with the following commands:

```bash
$ git tag v0.1.0  # Replace with new version
$ git push origin v0.1.0
```
