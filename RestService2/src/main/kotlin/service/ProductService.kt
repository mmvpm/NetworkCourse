package service

import dao.ProductDao
import dao.UserDao
import error.badRequest
import error.productNotFound
import error.userNotFound
import io.ktor.application.*
import io.ktor.features.*
import io.ktor.request.*
import io.ktor.response.*
import io.ktor.routing.*
import model.Product
import model.ProductTemplate
import model.Token
import model.User
import java.util.*

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
            route("user") {
                registerUser()
                signIn()
            }
        }

    // internal

    private val productDao = ProductDao()

    private val userDao = UserDao()

    private val timerByUserEmail = mutableMapOf<String, Timer?>()

    private fun createTimerTask(email: String) =
        object : TimerTask() {
            override fun run() {
                EmailSender.sendEmail(email)
            }
        }

    // GET: /product/{id}
    private fun Route.getProductById() =
        get("{id}") {
            val token = call.receiveOrNull<Token>()
            if (token == null) {
                userDao.findByIp(call.request.origin.remoteHost)?.let {
                    timerByUserEmail[it.email]?.cancel()
                    timerByUserEmail[it.email] = Timer()
                    timerByUserEmail[it.email]!!.schedule(createTimerTask(it.email), 1000L)
                }
            }
            val productId = call.parameters["id"] ?: return@get badRequest()
            val product = productDao.getById(productId, userDao.isKnownToken(token))
                ?: return@get productNotFound()
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
            val token = call.receiveOrNull<Token>()
            val product = call.receiveOrNull<Product>() ?: return@put badRequest()
            val updatedProduct = productDao.update(product, userDao.isKnownToken(token))
                ?: return@put productNotFound()
            call.respond(updatedProduct)
        }

    // DELETE: /product/delete/{id}
    private fun Route.deleteProductById() =
        delete("/delete/{id}") {
            val token = call.receiveOrNull<Token>()
            val productId = call.parameters["id"] ?: return@delete badRequest()
            val deletedProduct = productDao.deleteById(productId, userDao.isKnownToken(token))
                ?: return@delete productNotFound()
            call.respond(deletedProduct)
        }

    // GET: /products
    private fun Route.getAllProducts() =
        get {
            val token = call.receiveOrNull<Token>()
            if (token == null) {
                userDao.findByIp(call.request.origin.remoteHost)?.let {
                    timerByUserEmail[it.email]?.cancel()
                    timerByUserEmail[it.email] = Timer()
                    timerByUserEmail[it.email]!!.schedule(createTimerTask(it.email), 1000L)
                }
            }
            call.respond(
                if (userDao.isKnownToken(token))
                    productDao.getAllWithPrivate()
                else
                    productDao.getAllWithoutPrivate()
            )
        }

    // POST: /user/register
    private fun Route.registerUser() =
        post("register") {
            val newUser = call.receiveOrNull<User>() ?: return@post badRequest()
            val clientIp = call.request.origin.remoteHost
            val token = userDao.registerUser(newUser, clientIp)
            timerByUserEmail[newUser.email] = null
            call.respond(token)
        }

    // POST: /user/signIn
    private fun Route.signIn() =
        post("signIn") {
            val newUser = call.receiveOrNull<User>() ?: return@post badRequest()
            val token = userDao.signIn(newUser) ?: return@post userNotFound()
            call.respond(token)
        }
}