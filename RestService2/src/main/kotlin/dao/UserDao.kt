package dao

import model.Token
import model.User

class UserDao {

    fun registerUser(user: User): Token {
        users.add(user)
        return generateNewToken()
    }

    fun signIn(user: User): Token? =
        if (user in users)
            generateNewToken()
        else
            null

    fun isKnownToken(token: Token?) =
        token != null && token in knownTokens

    // internal

    private val users = mutableListOf<User>()

    private val knownTokens = mutableListOf<Token>()

    private fun generateNewToken(): Token {
        val newToken = Token.random()
        knownTokens.add(newToken)
        return newToken
    }
}