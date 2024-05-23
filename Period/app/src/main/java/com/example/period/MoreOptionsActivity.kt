package com.example.period.ui

import android.content.Intent
import android.os.Bundle
import android.widget.Button
import androidx.appcompat.app.AppCompatActivity
import com.example.period.R

class MoreOptionsActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.more_options_layout)

        val btnBookAppointment = findViewById<Button>(R.id.btnBookAppointment)
        val btnCycleInfo = findViewById<Button>(R.id.btnCycleInfo)
        val btnDeleteAccount = findViewById<Button>(R.id.btnDeleteAccount)

        btnBookAppointment.setOnClickListener {
            startActivity(Intent(this, AppointmentActivity::class.java))
        }
        btnCycleInfo.setOnClickListener {
            startActivity(Intent(this, CycleInfoActivity::class.java))
        }
        btnDeleteAccount.setOnClickListener {
            startActivity(Intent(this, DeleteAccountActivity::class.java))
        }
    }
}
