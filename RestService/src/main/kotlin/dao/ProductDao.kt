package dao

import model.Product
import model.ProductTemplate

class ProductDao {

    fun getById(id: String) = storage[id]

    fun getAll() = storage.values.toList()

    fun create(productTemplate: ProductTemplate): Product {
        val product = Product.fromTemplate(productTemplate)
        storage[product.id] = product
        return product
    }

    fun update(product: Product): Product? {
        deleteById(product.id) ?: return null
        storage[product.id] = product
        return product
    }

    fun deleteById(id: String) = storage.remove(id)

    // internal

    private val storage = mutableMapOf<String, Product>()
}