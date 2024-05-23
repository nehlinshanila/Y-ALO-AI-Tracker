package com.example.period.ui

import android.content.Intent
import android.os.Bundle
import android.widget.Button
import android.widget.CalendarView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.example.period.R
import java.util.Calendar

class WelcomeActivity : AppCompatActivity() {

    private var selectedDate: Long = -1

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.welcome_activity)

        val calendarView = findViewById<CalendarView>(R.id.calendarView)
        val logPeriodButton = findViewById<Button>(R.id.logPeriodButton)
        val moreOptionsButton = findViewById<Button>(R.id.moreOptionsButton)

        calendarView.setOnDateChangeListener { _, year, month, dayOfMonth ->
            selectedDate = Calendar.getInstance().apply {
                set(year, month, dayOfMonth)
            }.timeInMillis
        }

        logPeriodButton.setOnClickListener {
            if (selectedDate != -1L) {
                // Handle the logging period logic here
                Toast.makeText(this, "Period logged for the selected date.", Toast.LENGTH_SHORT).show()
            } else {
                Toast.makeText(this, "Please select a date first.", Toast.LENGTH_SHORT).show()
            }
        }

        moreOptionsButton.setOnClickListener {
            startActivity(Intent(this, MoreOptionsActivity::class.java))
        }
    }
}
