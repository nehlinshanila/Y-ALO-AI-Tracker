package com.example.period

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import com.example.period.R
import com.github.mikephil.charting.charts.BarChart
import com.github.mikephil.charting.data.BarData
import com.github.mikephil.charting.data.BarDataSet
import com.github.mikephil.charting.data.BarEntry

class CycleInfoActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.cycle_info_activity)

        val barChart = findViewById<BarChart>(R.id.chart)

        val entries = mutableListOf<BarEntry>()
        entries.add(BarEntry(1f, 3f))
        entries.add(BarEntry(2f, 5f))
        entries.add(BarEntry(3f, 2f))
        entries.add(BarEntry(4f, 4f))
        entries.add(BarEntry(5f, 6f))

        val dataSet = BarDataSet(entries, "Cycle Information")
        val data = BarData(dataSet)
        barChart.data = data
        barChart.invalidate() // Refresh chart
    }
}
