package model

import kotlinx.serialization.Serializable
import java.util.*

@Serializable
data class Token(val token: String) {
    companion object {
        fun random() = Token(UUID.randomUUID().toString())
    }
}
