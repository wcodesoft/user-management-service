## User Management proto package

This package holds the proto definition necessary to connect to the 
service and transport data using gRPC.

To use it on ``build.gradle.kts`` use it:

```bash
implementation("org.wcode.usermanagement:proto:0.0.1")
```

### Messages

```proto
message User {
  string username = 1;
  optional string firstName = 2;
  optional string lastName = 3;
  optional int32 age = 4;
}

message Response {
  bool success = 1;
}
```

### Services

```proto
rpc CreateUser(User) returns (Response);
```

### Usage

The package is being deployed on GitHub Registry. To use it's necessary
to define two environment variables on your system:

* GITHUB_ACTOR: username of the user trying to download the package
* GITHUB_TOKEN: access token created with at least read package permission