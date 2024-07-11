# gRPC UI for using gRPC services

This guide explains how to setup an open source tool to exercise the gRPC calls offered by a server. The demo section will be using an XR router as the server offering the [gNOI](https://github.com/openconfig/gnoi) services. For those who are new to gRPC, please follow the links in the overview section to fully understand all the technologies involved. gRPC UI is not recommended for gNMI since the encoding is not correctly handled by the tool.


## 1 Overview

### 1.1 What is gRPC
[gRPC](https://grpc.io/docs/what-is-grpc/introduction/) is an opensource framework for making Remote Procedure Calls. Services are defined using [Protocol Buffers](https://protobuf.dev/overview/) which form the basis for communication between clients and servers. Protocol Buffers make gRPC platform-neutral and language-neutral i.e client written in Go running on local machine can communicate with a server written in Python running as a Web service.


### 1.2 How do you use gRPC?

gRPC is meant as a communication mechanism between machines. As such the serialized procol buffers sent across machines are not human readable. gRPC offers JSON/XML encoding of the messages, but for complex service definitons this is still not easy for human interaction. Below are some of the tools which lets users test their services:

- [Postman](https://www.postman.com/product/what-is-postman/): Provides an App to send and receive messages for web services, as well as some level of automation. Recently added support for grpc. (not OpenSource) 
- [gRPCurl](https://github.com/fullstorydev/grpcurl#grpcurl): Generic CLI client which lets users pass requests to server.
- [gRPC UI](https://github.com/fullstorydev/grpcui#grpc-ui): Web UI providees an UI which uses gRPCurl 
- [Ondatra](https://github.com/openconfig/ondatra): Automation framework from OpenConfig project for running Go based tests against devices.
- Write your own client: This is what usually happens when developing your own service.


### 1.3 What is gRPC UI

[gRPC UI](https://github.com/fullstorydev/grpcui) is an open source tool written in Go and Javascript. It gives the users a Web UI to interact easily with a server that is running. Given a service definition, it will provide a webform where users can fill in exactly the details required to send a request and receive the response.


## 2. Steps

The following steps are done from your host (ex: `host-1234`) and from location (ex: `/xyz/grpcui/`).

### 2.1 Installing GRPCUI on host

Install gRPC UI

```bash
host-1234:/xyz/grpcui/ $ export GOROOT="~/go/1.19.4"
host-1234:/xyz/grpcui/ $ export GOPATH="~/.go" 
host-1234:/xyz/grpcui/ $ alias go="$GOROOT/bin/go"
host-1234:/xyz/grpcui/ $ alias grpcui="$GOPATH/bin/grpcui"
host-1234:/xyz/grpcui/ $ go install github.com/fullstorydev/grpcui/cmd/grpcui@latest
```

Usage:
```bash
host-1234:/xyz/grpcui/ $ grpcui -help
Usage:
...
```

### 2.1x Skip install with Docker

gRPCUI is available as a docker container as well. This can be used to skip the installation step. Select docker.io when prompted for the first time.

```bash
host-1234:/xyz/grpcui/ $ docker run --rm --net=host -P fullstorydev/grpcui:v1.3.1 -help
Emulate Docker CLI using podman. Create /etc/containers/nodocker to quiet msg.
✔ docker.io/fullstorydev/grpcui:v1.3.1
Trying to pull docker.io/fullstorydev/grpcui:v1.3.1...
Getting image source signatures
Copying blob 31ee24cbf56f done  
Copying blob 441643a1ba34 done  
Copying blob 10b0b9d2f1a5 done  
Copying config 83ea6dec6e done  
Writing manifest to image destination
Storing signatures
Usage:
...
```

### 2.2 Generating a protoset

gRPC UI requries a proto or a protoset to determine understand the service defintions offered by the server. We will use protoset generated from the proto files for this demo. These protoset files can be reused as long as it matches the version of service the server implements.


Identify and clone the repositories which provide your proto. For example: system.proto from [gNOI system](https://github.com/openconfig/gnoi/blob/main/system/system.proto)


It includes some proto from `gnoi/common` and `gnoi/types`. `gnoi/types` imports from protocolbuffers/protobuf.git

```bash
host-1234:/xyz/grpcui/ $ git clone https://github.com/openconfig/gnoi.git
host-1234:/xyz/grpcui/ $ git clone https://github.com/protocolbuffers/protobuf.git
host-1234:/xyz/grpcui/ $ /usr/bin/protoc --include_imports --descriptor_set_out=system.desc -I./gnoi/ -I./protobuf/src gnoi/system/system.proto
```
This should generate the file `/xyz/grpcui/system.desc`


### 2.3 Connecting to your server and launching UI

Run this on the host using the protoset from step 2.2 and the IP/port of your grpc service. This will output a link that can be opened from your browser.
```bash
host-1234:/xyz/grpcui/ $ grpcui -plaintext -open-browser=false -protoset /xyz/grpcui/system.desc -bind $HOSTNAME -port 9090 172.26.228.36:65168
gRPC Web UI available at http://host-1234:9090/
```

Docker alternative:
```bash
host-1234:/xyz/grpcui/ $ docker run --rm --net=host -P -v /xyz/grpcui:/xyz/grpcui fullstorydev/grpcui:v1.3.1 -plaintext -open-browser=false -protoset /xyz/grpcui/system.desc -bind $HOSTNAME -port 9090 172.26.228.36:65168
gRPC Web UI available at http://host-1234:9090/
```

Open `http://host-1234:9090/` on a browser to use the services.


### 2.4 Using the system.proto services:

Pick a service and method from the drop down

      Service name: gnoi.system.System
      Method name: Ping


Provide metadata for authentication. Click the "+ Add item" button to add more entries

      username: **** 
      password: ****



Fill in the details required for by the proto request and click invoke


The Response Tab will contain the response in JSON. The request in JSON and the equivalent gRPCurl command is available in a another tab.


## 3 Additional Info

### 3.1 Setting up your gRPC services

The [gRPC website](https://grpc.io/docs/languages/) provides guides on how to setup your own services in different languages. You can follow along to create a sample server and client using python. You can find latest python versions here `/sw/packages/xrbuild-python/` and create a virtual env as below on the host

```bash
host-1234:/xyz/grpcui/ $ /usr/bin/python3 -m venv /xyz/grpcui/py
host-1234:/xyz/grpcui/ $ source /xyz/grpcui/py/bin/activate
(py)host-1234:/xyz/grpcui/ $ python3 -m pip install --upgrade pip grpcio grpcio-tools mypy-protobuf
```

### 3.2 Reflection service

Reflection feature allows servers to advertise the supported protoset file, so that the client does not need to generate the file on its own. When creating your own gRPC server, you can enable this feature as a separate service which will communicate the protoset file to the client.

