package service

import dao.ProductDao
import error.badRequest
import error.productNotFound
import io.ktor.application.*
import io.ktor.request.*
import io.ktor.response.*
import io.ktor.routing.*
import model.Product
import model.ProductTemplate

object ProductService {

    fun Application.productRouting() =
        routing {
            route("/product") {
                getProductById()
                createProduct()
                upsertProduct()
                deleteProductById()
            }
            route("products") {
                getAllProducts()
            }
        }

    // internal

    private val productDao = ProductDao()

    // GET: /product/{id}
    private fun Route.getProductById() =
        get("{id}") {
            val productId = call.parameters["id"] ?: return@get badRequest()
            val product = productDao.getById(productId) ?: return@get productNotFound()
            call.respond(product)
        }

    // POST: /product/create
    private fun Route.createProduct() =
        post("create") {
            val productTemplate = call.receiveOrNull<ProductTemplate>() ?: return@post badRequest()
            val createdProduct = productDao.create(productTemplate)
            call.respond(createdProduct)
        }

    // PUT: /product/update
    private fun Route.upsertProduct() =
        put("update") {
            val product = call.receiveOrNull<Product>() ?: return@put badRequest()
            val updatedProduct = productDao.update(product) ?: return@put productNotFound()
            call.respond(updatedProduct)
        }

    // DELETE: /product/delete/{id}
    private fun Route.deleteProductById() =
        delete("/delete/{id}") {
            val productId = call.parameters["id"] ?: return@delete badRequest()
            val deletedProduct = productDao.deleteById(productId) ?: return@delete productNotFound()
            call.respond(deletedProduct)
        }

    // GET: /products
    private fun Route.getAllProducts() =
        get {
            call.respond(productDao.getAll())
        }
}