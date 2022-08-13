package com.example.snapsheetandroid

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.LinearLayout
import android.widget.TextView
import android.widget.Toast
import com.github.kittinunf.fuel.Fuel
import com.github.kittinunf.result.Result
import org.json.JSONArray
import org.json.JSONObject

class CourseActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_course)

       val main_layout = findViewById<LinearLayout>(R.id.linearlayout)

       val username = intent.getStringExtra("username")
        val email = intent.getStringExtra("email")
        Toast.makeText(this,username,Toast.LENGTH_SHORT).show()

        Fuel.get("http://192.168.50.146:8000/API/Get_Users_Courses/?username=" + username).response(){request, response, result ->

            when(result)
            {
                is Result.Success ->{
                    println(response)
                    println(String(response.data))

                    val jsonarray = JSONArray(String(response.data))

                    for( i in 0 until jsonarray.length())
                    {
                        val jsonobject = jsonarray.getJSONObject(i)

                        val course_layout = layoutInflater.inflate(R.layout.course_layout,null)

                        course_layout.findViewById<TextView>(R.id.semester).setText(jsonobject.get("SemesterCode").toString())
                        course_layout.findViewById<TextView>(R.id.courseid).setText(jsonobject.get("CourseCode").toString())
                        course_layout.findViewById<TextView>(R.id.coursename).setText(jsonobject.get("Description").toString())
                        course_layout.findViewById<TextView>(R.id.section).setText(jsonobject.get("Section").toString())

                        course_layout.setOnClickListener(){
                            val nextpage = Intent(this,CameraActivity::class.java)
                            nextpage.putExtra("semester",jsonobject.get("SemesterCode").toString())
                            nextpage.putExtra("courseid",jsonobject.get("CourseCode").toString())
                            nextpage.putExtra("coursename",jsonobject.get("Description").toString())
                            nextpage.putExtra("section",jsonobject.get("Section").toString())
                            nextpage.putExtra("index",i.toString())
                            nextpage.putExtra("json",String(response.data))
                            nextpage.putExtra("username",username)
                            nextpage.putExtra("email",email)
                            nextpage.putExtra("sheetlink",jsonobject.get("SheetLink").toString())


                            startActivity(nextpage)
                        }

                        main_layout.addView(course_layout)

                    }


                }
                is Result.Failure ->{
                    println(response)
                    println(String(response.data))
                }
            }
        }


    }
}