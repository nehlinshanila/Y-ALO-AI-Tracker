package com.example.period

import android.content.Intent
import android.os.Bundle
import android.util.Log
import android.widget.Button
import android.widget.EditText
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.auth.PhoneAuthCredential
import com.google.firebase.auth.PhoneAuthProvider

class VerificationActivity : AppCompatActivity() {
    private lateinit var auth: FirebaseAuth
    private lateinit var codeInput: EditText
    private lateinit var verifyButton: Button
    private lateinit var verificationId: String

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.verification_activity)

        auth = FirebaseAuth.getInstance()

        codeInput = findViewById(R.id.codeInput)
        verifyButton = findViewById(R.id.verifyButton)

        verificationId = intent.getStringExtra("verificationId") ?: ""

        verifyButton.setOnClickListener {
            val code = codeInput.text.toString()
            if (code.isNotEmpty()) {
                val credential = PhoneAuthProvider.getCredential(verificationId, code)
                signInWithPhoneAuthCredential(credential)

            } else {
                Toast.makeText(this, "Please enter the verification code", Toast.LENGTH_SHORT).show()
            }
        }
    }

    private fun signInWithPhoneAuthCredential(credential: PhoneAuthCredential) {
        auth.signInWithCredential(credential)
            .addOnCompleteListener(this) { task ->
                if (task.isSuccessful) {
                    Log.d("VerificationActivity", "signInWithCredential:success")
                    startActivity(Intent(this, WelcomeActivity::class.java))
                    finish()
                } else {
                    Log.w("VerificationActivity", "signInWithCredential:failure", task.exception)
                    Toast.makeText(this, "Verification failed: ${task.exception?.message}", Toast.LENGTH_SHORT).show()
                }
            }
    }
}
