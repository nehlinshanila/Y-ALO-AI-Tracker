package com.example.period

import android.content.Intent
import android.os.Bundle
import android.util.Log
import android.widget.Button
import android.widget.CalendarView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.example.period.R
import com.google.firebase.Firebase
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.database.DatabaseReference
import com.google.firebase.database.FirebaseDatabase
import com.google.firebase.database.database
import java.util.Calendar

class WelcomeActivity : AppCompatActivity() {

    private var selectedDate: Long = -1
    private lateinit var selectedDateText: String
    private lateinit var database: DatabaseReference
    private lateinit var auth: FirebaseAuth

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.welcome_activity)

        auth = FirebaseAuth.getInstance()
        database = FirebaseDatabase.getInstance("https://y-alo-4d6f6-default-rtdb.asia-southeast1.firebasedatabase.app/").reference
//        database = Firebase.database.getReferenceFromUrl("https://y-alo-4d6f6-default-rtdb.asia-southeast1.firebasedatabase.app/")

        val calendarView = findViewById<CalendarView>(R.id.calendarView)
        val logPeriodButton = findViewById<Button>(R.id.logPeriodButton)
        val moreOptionsButton = findViewById<Button>(R.id.moreOptionsButton)

        calendarView.setOnDateChangeListener { _, year, month, dayOfMonth ->
            selectedDate = Calendar.getInstance().apply {
                set(year, month, dayOfMonth)
            }.timeInMillis

            selectedDateText = "$year-${month + 1}-$dayOfMonth"
        }

        logPeriodButton.setOnClickListener {
            if (selectedDate != -1L) {
                // Handle the logging period logic here
                logPeriod()
                Toast.makeText(this, "Period logged for the selected date.", Toast.LENGTH_SHORT).show()
            } else {
                Toast.makeText(this, "Please select a date first.", Toast.LENGTH_SHORT).show()
            }
        }

        moreOptionsButton.setOnClickListener {
            startActivity(Intent(this, MoreOptionsActivity::class.java))
        }
    }

    private fun logPeriod() {
        val userId = auth.currentUser?.uid
        if (userId != null) {
            val logDate = mapOf("selectedDate" to selectedDateText)
            Log.i("Firebase", "Period logged for the selected date:$logDate and UID:$userId")
            val userRef = database.child(userId).child("periodLogs")
            userRef.push().setValue(logDate)
                .addOnSuccessListener {
                        Toast.makeText(this, "Period logged for the selected date.", Toast.LENGTH_SHORT).show()
                    }
                .addOnFailureListener{ exception ->
                        Toast.makeText(this, "Failed to log period: ${exception.message}", Toast.LENGTH_SHORT).show()
                    }
                }
        }
}
