package com.example.snapsheetandroid

import android.app.Activity
import android.content.ActivityNotFoundException
import android.content.ContentValues.TAG
import android.content.Intent
import android.content.pm.PackageManager
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.media.Image
import android.net.Uri
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.os.Environment
import android.os.Environment.getExternalStoragePublicDirectory
import android.provider.MediaStore
import android.util.Log
import android.widget.Button
import android.widget.ImageView
import android.widget.Toast
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
import com.google.android.gms.auth.api.signin.GoogleSignIn


import com.google.android.gms.auth.api.signin.GoogleSignInOptions
import com.google.android.gms.auth.api.signin.GoogleSignInAccount
import com.google.android.gms.common.SignInButton
import com.google.android.gms.tasks.Task
import com.google.android.gms.common.api.ApiException
import org.json.JSONArray
import org.json.JSONObject


class MainActivity : AppCompatActivity() {
    val RC_SIGN_IN = 5
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.sign_in)


        val gso = GoogleSignInOptions.Builder(GoogleSignInOptions.DEFAULT_SIGN_IN)
            .requestIdToken("1051132029790-i1ppjir19u8tbj784n6u8f18gkn2a1kd.apps.googleusercontent.com")
            .requestEmail()
            .build()
        val mGoogleSignInClient = GoogleSignIn.getClient(this, gso);

        val sign_in_button = findViewById<SignInButton>(R.id.sign_in_button)

        sign_in_button.setOnClickListener(){
            val signInIntent = mGoogleSignInClient.getSignInIntent();
            startActivityForResult(signInIntent, RC_SIGN_IN);
        }







    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)

        // Result returned from launching the Intent from GoogleSignInClient.getSignInIntent(...);
        if (requestCode == RC_SIGN_IN) {
            // The Task returned from this call is always completed, no need to attach
            // a listener.
            val task: Task<GoogleSignInAccount> = GoogleSignIn.getSignedInAccountFromIntent(data)
            handleSignInResult(task)
        }
    }

    private fun handleSignInResult(completedTask: Task<GoogleSignInAccount>) {
        try {
            val account = completedTask.getResult(ApiException::class.java)

            Fuel.get("http://192.168.50.146:8000/API/verify_user/?id_token=" + account.idToken).response(){
                request, response, result ->

                when(result)
                {
                    is Result.Success ->{
                        Toast.makeText(this,"Login successfull",Toast.LENGTH_SHORT).show()
                        println("This is response data: " + String(response.data))

                        Log.d("Response",response.toString())
                        val json = JSONObject(String(response.data))


                        val next_page = Intent(this,CourseActivity::class.java)
                        next_page.putExtra("username",json.get("username").toString())
                        next_page.putExtra("email",account.email)
                        startActivity(next_page)

                    }

                    is Result.Failure ->{
                        Toast.makeText(this,"Login unsuccessfull",Toast.LENGTH_LONG).show()
                        println(response.toString())
                    }
                }
            }

            // Signed in successfully, show authenticated UI.

        } catch (e: ApiException) {
            // The ApiException status code indicates the detailed failure reason.
            // Please refer to the GoogleSignInStatusCodes class reference for more information.
            Log.w(TAG, "signInResult:failed code=" + e.statusCode)

        }
    }





}