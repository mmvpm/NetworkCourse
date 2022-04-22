import java.net.*

fun isAvailable(address: InetAddress, port: Int) =
    runCatching { Socket(address, port).close() }.isFailure

fun getAvailablePorts(address: InetAddress, from: Int = 0, to: Int = 65535) = sequence {
    for (port in from..to) {
        if (isAvailable(address, port))
            yield(port)
    }
}

fun main() {
    val ip = "192.168.0.101"
    val inetAddress = InetAddress.getByName(ip)
    print("available ports: ")
    getAvailablePorts(inetAddress, 10000, 10010).forEach {
        print("$it ")
    }
}