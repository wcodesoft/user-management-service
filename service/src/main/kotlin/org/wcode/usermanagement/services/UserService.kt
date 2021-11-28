package org.wcode.usermanagement.services

import com.google.protobuf.Empty
import io.grpc.stub.StreamObserver
import io.quarkus.grpc.GrpcService
import org.wcode.usermanagement.proto.UserManagementServiceGrpc
import org.wcode.usermanagement.proto.UserOuterClass.*

@GrpcService
class UserService : UserManagementServiceGrpc.UserManagementServiceImplBase() {

    private val users = mutableMapOf<String,User>()

    override fun createUser(
        request: User?,
        responseObserver: StreamObserver<Response>
    ) {
        request?.apply {
            users.putIfAbsent(this.username,this)
        }
        responseObserver.apply {
            val response = Response.newBuilder().apply {
                success = true
            }.build()
            onNext(response)
            onCompleted()
        }
    }

    override fun getAllUsers(request: Empty?, responseObserver: StreamObserver<GetAllUsersResponse>) {
        responseObserver.apply {
            val response = GetAllUsersResponse.newBuilder().apply {
                addAllUsers(users.map { it.value })
            }.build()
            onNext(response)
            onCompleted()
        }
    }
}