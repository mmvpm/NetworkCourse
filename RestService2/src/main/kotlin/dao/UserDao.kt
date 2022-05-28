package dao

import model.Token
import model.User

class UserDao {

    fun registerUser(user: User, clientIp: String): Token {
        users.add(user.copy(ip = clientIp))
        return generateNewToken()
    }

    fun signIn(user: User): Token? =
        if (user in users)
            generateNewToken()
        else
            null

    fun isKnownToken(token: Token?) =
        token != null && token in knownTokens

    fun findByIp(clientIp: String) =
        users.firstOrNull { user ->
            user.ip == clientIp
        }

    // internal

    private val users = mutableListOf<User>()

    private val knownTokens = mutableListOf<Token>()

    private fun generateNewToken(): Token {
        val newToken = Token.random()
        knownTokens.add(newToken)
        return newToken
    }
}