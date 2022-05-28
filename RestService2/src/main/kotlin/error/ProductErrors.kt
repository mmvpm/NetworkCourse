package error

import io.ktor.application.*
import io.ktor.http.*
import io.ktor.response.*
import io.ktor.util.pipeline.*

// 400 Bad Request
suspend fun PipelineContext<Unit, ApplicationCall>.badRequest() =
    call.respondText("Bad Request", status = HttpStatusCode.BadRequest)

// 404 NotFound
suspend fun PipelineContext<Unit, ApplicationCall>.productNotFound() =
    call.respondText("Product Not Found", status = HttpStatusCode.NotFound)

// 404 NotFound
suspend fun PipelineContext<Unit, ApplicationCall>.userNotFound() =
    call.respondText("User Not Found", status = HttpStatusCode.NotFound)
