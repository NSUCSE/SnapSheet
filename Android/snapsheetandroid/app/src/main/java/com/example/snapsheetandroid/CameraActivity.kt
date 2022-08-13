package com.example.snapsheetandroid

import android.app.Activity
import android.content.ActivityNotFoundException
import android.content.Intent
import android.content.pm.PackageManager
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.graphics.Color
import android.media.Image
import android.net.Uri
import android.opengl.Visibility
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.os.Environment
import android.os.Environment.getExternalStoragePublicDirectory
import android.provider.MediaStore
import android.view.View
import android.widget.*
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import androidx.core.content.FileProvider
import java.io.File
import java.io.IOException
import java.text.SimpleDateFormat
import java.util.*
import java.util.jar.Manifest
import com.github.kittinunf.fuel.Fuel
import com.github.kittinunf.result.Result
import org.json.JSONArray
import org.json.JSONObject
import org.w3c.dom.Text

class CameraActivity : AppCompatActivity() {
    val REQUEST_IMAGE_CAPTURE = 1
    lateinit var currentPhotoPath: String
    lateinit var imageView: ImageView
    lateinit var id:EditText
    lateinit var marks:EditText
    var res_id = -1
    var res_marks = -1

    var assessment:String = ""

    var photoFile: File? = null


    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val click = findViewById<Button>(R.id.click)
        click.setOnClickListener(){
            dispatchTakePictureIntent()
        }
        val semester = intent.getStringExtra("semester")
        val courseid = intent.getStringExtra("courseid")
        val coursename = intent.getStringExtra("coursename")
        val section = intent.getStringExtra("section")
        val index:Int = intent.getStringExtra("index")!!.toInt()
        val username = intent.getStringExtra("username")
        val email = intent.getStringExtra("email")
        val sheetlink = intent.getStringExtra("sheetlink")


        val assessment_submit_button = findViewById<Button>(R.id.submit_button)
        assessment_submit_button.setOnClickListener(){

            Fuel.get("http://192.168.50.146:8000/API/update_google_sheet/?username="+username+"&student_id="+id.text+"&CourseCode="+courseid+"&SemesterCode="+semester+"&Section="+section+"&Marks="+marks.text+"&Assessment="+assessment)
                .response(){request, response, result ->

                    when(result)
                    {
                        is Result.Success ->{
                            Toast.makeText(this,"Updated successfully",Toast.LENGTH_SHORT).show()
                        }
                        is Result.Failure ->{
                            Toast.makeText(this,"Something went wrong, please try again.",Toast.LENGTH_SHORT).show()
                        }
                    }

                }

        }

        val quizzes = findViewById<LinearLayout>(R.id.quizzes)
        val selected = findViewById<TextView>(R.id.selected)

        imageView = findViewById<ImageView>(R.id.imageView)


        val jsonarray = JSONArray(intent.getStringExtra("json"))



           val jsonobject = jsonarray.getJSONObject(index)
           val arr = jsonobject.getJSONArray("Assessments")

            for(i in 0 until arr.length())
            {
                println("this is " + arr[i])
                val quiz = layoutInflater.inflate(R.layout.quiz,null)

                val quiz_textview = quiz.findViewById<TextView>(R.id.quiz)
                quiz_textview.setText(arr[i].toString())

                quiz.setOnClickListener(){
                    selected.setText("Selected: "+ arr[i].toString())
                    assessment = arr[i].toString()
                }

                quizzes.addView(quiz)


            }



    }



    @Throws(IOException::class)
    private fun createImageFile(): File {
        // Create an image file name
        val timeStamp = SimpleDateFormat("yyyyMMdd_HHmmss").format(Date())
        val imageFileName = "SnapSheet_" + timeStamp + "_"
        val storageDir = getExternalFilesDir(Environment.DIRECTORY_PICTURES)
        val image = File.createTempFile(
            imageFileName, /* prefix */
            ".jpg", /* suffix */
            storageDir      /* directory */
        )

        // Save a file: path for use with ACTION_VIEW intents
        currentPhotoPath = image.absolutePath
        return image
    }

    private fun dispatchTakePictureIntent() {
        Intent(MediaStore.ACTION_IMAGE_CAPTURE).also { takePictureIntent ->
            // Ensure that there's a camera activity to handle the intent
            takePictureIntent.resolveActivity(packageManager)?.also {
                // Create the File where the photo should go
                photoFile = try {
                    createImageFile()
                } catch (ex: IOException) {
                    // Error occurred while creating the File
                    null
                }
                // Continue only if the File was successfully created
                photoFile?.also {
                    val photoURI: Uri = FileProvider.getUriForFile(
                        this,
                        "com.example.snapsheetandroid.fileprovider",
                        it)

                    takePictureIntent.putExtra(MediaStore.EXTRA_OUTPUT, photoURI)
                    startActivityForResult(takePictureIntent, REQUEST_IMAGE_CAPTURE)
                }
            }
        }
    }


    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)

        if (requestCode == REQUEST_IMAGE_CAPTURE && resultCode == Activity.RESULT_OK) {
            val myBitmap = BitmapFactory.decodeFile(photoFile!!.absolutePath)


            imageView.setImageBitmap(myBitmap)


            var bytearray = File(photoFile!!.absolutePath).readBytes()

            Toast.makeText(this,"Processing request",Toast.LENGTH_SHORT).show()

            Fuel.post("https://api.apilayer.com/image_to_text/upload")
                .header("apikey","xNe85ZKCeaW6PJlJcSfMFYadvwzPxFnn")
                .body(File(photoFile!!.absolutePath).readBytes())
                .response { request,response,result ->
                    when(result)
                    {
                        is Result.Success ->{
                            Toast.makeText(this,"request success",Toast.LENGTH_LONG).show()
                            println(response)
                            println("Response data:")
                            println(String(response.data))

                            val strs = JSONObject(String(response.data)).getJSONArray("annotations")
                            var res:String = ""

                            for( i in 0 until strs.length())
                            {
                               println(strs[i])

                                val str = strs[i].toString()

                                for(j in 0 until str.length)
                                {
                                    if(str[j]>='0' && str[j]<='9')
                                    {
                                        res += str[j]
                                    }
                                }


                            }
                            println("result is " + res)
                            id = findViewById<EditText>(R.id.student_id)
                            marks = findViewById<EditText>(R.id.marks)
                            id.setText( res.substring(0,10))
                            marks.setText( res.subSequence(10,res.length))
                            id.visibility = View.VISIBLE
                            marks.visibility = View.VISIBLE



                        }
                        is Result.Failure ->{
                            Toast.makeText(this,"request failed",Toast.LENGTH_LONG).show()
                        }

                    }
                }

        } else {

        }
    }


}