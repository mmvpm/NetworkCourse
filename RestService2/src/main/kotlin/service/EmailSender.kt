package service

import org.apache.commons.mail.DefaultAuthenticator
import org.apache.commons.mail.Email
import org.apache.commons.mail.SimpleEmail
import java.io.File

object EmailSender {
    fun sendEmail(toEmail: String) {
        val auth = File("auth.txt").readText().split(' ')
        val email: Email = SimpleEmail()
        email.hostName = "smtp.mail.ru"
        email.setSmtpPort(465)
        email.setAuthenticator(DefaultAuthenticator(auth[0], auth[1]))
        email.isSSLOnConnect = true
        email.setFrom(auth[0])
        email.subject = "Rest Service"
        email.setMsg("Рады видеть вас в нашем сервисе вновь!")
        email.addTo(toEmail)
        email.send()
    }
}
