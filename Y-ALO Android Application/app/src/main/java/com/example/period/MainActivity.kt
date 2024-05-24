package com.example.period

import android.app.Application
import com.google.firebase.FirebaseApp
import com.google.firebase.database.FirebaseDatabase
import android.content.Intent
import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        // Check if the user is registered. This is just a placeholder.
        val isRegistered = checkUserRegistration()

        if (isRegistered) {
            startActivity(Intent(this, WelcomeActivity::class.java))
        } else {
            startActivity(Intent(this, RegisterActivity::class.java))
        }

        finish() // Close MainActivity
    }

    private fun checkUserRegistration(): Boolean {
        // Simple logic to check registration status (for debugging purposes)
        val sharedPreferences = getSharedPreferences("app_preferences", MODE_PRIVATE)
        return sharedPreferences.getBoolean("is_registered", false)
    }
}



class MyApplication : Application() {
    override fun onCreate() {
        super.onCreate()
        FirebaseApp.initializeApp(this)
        FirebaseDatabase.getInstance().setPersistenceEnabled(true) // Optional: enable offline capabilities
    }
}
