package model

import kotlinx.serialization.Serializable

@Serializable
data class ProductTemplate(
    val name: String,
    val description: String,
    val icon: String,
    val token: String? = null
)