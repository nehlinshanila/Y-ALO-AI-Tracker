package com.example.period

import android.content.Intent
import android.os.Bundle
import android.util.Log
import android.widget.Button
import android.widget.EditText
import android.widget.Spinner
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.example.period.model.User
import com.google.firebase.FirebaseException
import com.google.firebase.FirebaseTooManyRequestsException
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.auth.FirebaseAuthInvalidCredentialsException
import com.google.firebase.auth.FirebaseAuthMissingActivityForRecaptchaException
import com.google.firebase.auth.FirebaseAuthWebException
import com.google.firebase.auth.PhoneAuthCredential
import com.google.firebase.auth.PhoneAuthOptions
import com.google.firebase.auth.PhoneAuthProvider
import com.google.firebase.database.DatabaseReference
import com.google.firebase.database.FirebaseDatabase
import java.util.concurrent.TimeUnit

class RegisterActivity : AppCompatActivity() {
    private lateinit var auth: FirebaseAuth
    private lateinit var database: DatabaseReference
    private lateinit var phoneInput: EditText
    private lateinit var nameInput: EditText
    private lateinit var languageSpinner: Spinner
    private lateinit var registerButton: Button

    private lateinit var verificationId: String

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.register_activity)

        auth = FirebaseAuth.getInstance()
        database = FirebaseDatabase.getInstance().reference

        phoneInput = findViewById(R.id.phoneInput)
        nameInput = findViewById(R.id.nameInput)
        languageSpinner = findViewById(R.id.languageSpinner)
        registerButton = findViewById(R.id.registerButton)


        registerButton.setOnClickListener {

            val phoneNumber = phoneInput.text.toString()
            if (phoneNumber.isNotEmpty()) {
                sendVerificationCode(phoneNumber)
            } else {
                Toast.makeText(this, "Please enter a phone number", Toast.LENGTH_SHORT).show()
            }
        }
    }

    private fun sendVerificationCode(phoneNumber: String) {
        val options = PhoneAuthOptions.newBuilder(auth)
            .setPhoneNumber("+88$phoneNumber")
            .setTimeout(60L, TimeUnit.SECONDS)
            .setActivity(this)
            .setCallbacks(object : PhoneAuthProvider.OnVerificationStateChangedCallbacks() {
                override fun onVerificationCompleted(credential: PhoneAuthCredential) {
                    Log.d("RegisterActivity", "Verification completed: ${credential.smsCode}")
                    Toast.makeText(this@RegisterActivity, "Verification completed", Toast.LENGTH_SHORT).show()
//                    signInWithPhoneAuthCredential(credential)
                }

                override fun onVerificationFailed(e: FirebaseException) {
                    Log.e("RegisterActivity", "Verification failed", e)

                    val errorMessage = when (e) {
                        is FirebaseAuthInvalidCredentialsException -> {
                            "Invalid request: ${e.message}"
                        }
                        is FirebaseTooManyRequestsException -> {
                            "SMS quota exceeded: ${e.message}"
                        }
                        is FirebaseAuthMissingActivityForRecaptchaException -> {
                            "reCAPTCHA verification failed: ${e.message}"
                        }
                        is FirebaseAuthWebException -> {
                            "Web exception occurred: ${e.message}"
                        }
                        else -> {
                            "Verification failed: ${e.message}"
                        }
                    }

                    Toast.makeText(this@RegisterActivity, errorMessage, Toast.LENGTH_SHORT).show()
                }

                override fun onCodeSent(verificationId: String, token: PhoneAuthProvider.ForceResendingToken) {
                    Log.d("RegisterActivity", "Code sent: $verificationId")
                    this@RegisterActivity.verificationId = verificationId
                    startActivity(Intent(this@RegisterActivity, VerificationActivity::class.java).putExtra("verificationId", verificationId))
                }
            })
            .build()
        PhoneAuthProvider.verifyPhoneNumber(options)
    }

    private fun signInWithPhoneAuthCredential(credential: PhoneAuthCredential) {
        auth.signInWithCredential(credential)
            .addOnCompleteListener(this) { task ->
                if (task.isSuccessful) {
                    Log.d("RegisterActivity", "signInWithCredential:success")
                    // Registration success, save user data to Firebase
                    saveUserData()
                } else {
                    Log.w("RegisterActivity", "signInWithCredential:failure", task.exception)
                    Toast.makeText(this, "Registration failed: ${task.exception?.message}", Toast.LENGTH_SHORT).show()
                }
            }
    }

    private fun saveUserData() {
        val name = nameInput.text.toString()
        val phoneNumber = phoneInput.text.toString()
        val language = languageSpinner.selectedItem.toString()

        val user = User(name, phoneNumber, language)
        val userId = auth.currentUser?.uid

        userId?.let {
            database.child("users").child(it).setValue(user).addOnCompleteListener { task ->
                if (task.isSuccessful) {
                    Log.d("RegisterActivity", "User data saved successfully")
                    // Navigate to WelcomeActivity
                    startActivity(Intent(this, WelcomeActivity::class.java))
                    finish()
                } else {
                    Log.e("RegisterActivity", "Failed to save user data", task.exception)
                    Toast.makeText(this, "Failed to save user data: ${task.exception?.message}", Toast.LENGTH_SHORT).show()
                }
            }
        }
    }
}
