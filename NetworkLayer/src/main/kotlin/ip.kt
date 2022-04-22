import java.net.*
import kotlin.math.min

val InterfaceAddress.ip: String
    get() = this.address.hostAddress

val InterfaceAddress.mask: String
    get() =
        (0 until 32 step 8).joinToString(separator =  ".") { shift ->
            val zerosNumber = 8 - min(8, this.networkPrefixLength - shift)
            "${255 shr zerosNumber shl zerosNumber}"
        }

fun main() {
    val interfaceAddress = NetworkInterface
        .getByInetAddress(Inet4Address.getLocalHost())
        .interfaceAddresses[0]
    println("ip: ${interfaceAddress.ip}")
    println("mask: ${interfaceAddress.mask}")
}