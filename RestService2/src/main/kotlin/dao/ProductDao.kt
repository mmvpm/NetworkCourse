package dao

import model.Product
import model.ProductTemplate

class ProductDao {

    fun getById(id: String, withPrivate: Boolean): Product? {
        val product = storage[id]
        return if (withPrivate || product?.token == null)
            product?.removeToken()
        else
            null
    }

    fun getAllWithPrivate() =
        storage.values.map { product ->
            product.removeToken()
        }

    fun getAllWithoutPrivate() =
        storage.values.filter { product ->
            product.token == null
        }

    fun create(productTemplate: ProductTemplate): Product {
        val product = Product.fromTemplate(productTemplate)
        storage[product.id] = product
        return product
    }

    fun update(product: Product, withPrivate: Boolean): Product? {
        deleteById(product.id, withPrivate) ?: return null
        storage[product.id] = product
        return product
    }

    fun deleteById(id: String, withPrivate: Boolean) =
        if (withPrivate || storage[id]?.token == null)
            storage.remove(id)
        else
            null

    // internal

    private val storage = mutableMapOf<String, Product>()
}