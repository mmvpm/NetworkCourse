package model

import kotlinx.serialization.Serializable

@Serializable
data class Product(
    val id: String,
    val name: String,
    val description: String,
    val icon: String,
    val token: String? = null
) {
    companion object {
        private var nextId = 0

        fun fromTemplate(template: ProductTemplate): Product {
            nextId += 1
            return Product(nextId.toString(), template.name, template.description, template.icon, template.token)
        }
    }

    fun removeToken() = this.copy(token = null)
}
