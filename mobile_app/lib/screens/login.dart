import 'package:flutter/material.dart';
import 'package:mobile_app/services/auth.dart';
import 'package:mobile_app/size_config.dart';

class LoginScreen extends StatefulWidget {
  LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  TextEditingController emailController = TextEditingController();
  TextEditingController passwordController = TextEditingController();
  bool showPassword = false;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(18.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.spaceAround,
            children: <Widget>[
              Image.asset(
                'assets/BlindVision Icon.png',
                width: 200,
                height: 200,
                fit: BoxFit.fill,
              ),
              const Text('BlindVision', style: TextStyle(fontSize: 45)),
              TextField(
                controller: emailController,
                decoration: const InputDecoration(labelText: 'Email'),
              ),
              Row(
                children: [
                  SizedBox(
                    width: SizeConfig.blockSizeHorizontal! * 80,
                    child: TextField(
                      obscureText: !showPassword,
                      controller: passwordController,
                      decoration: const InputDecoration(labelText: 'Password'),
                    ),
                  ),
                  SizedBox(
                    width: SizeConfig.blockSizeHorizontal! * 10,
                    child: IconButton(
                      icon: const Icon(Icons.remove_red_eye_rounded),
                      onPressed: () {
                        setState(() {
                          showPassword = !showPassword;
                        });
                      },
                    ),
                  )
                ],
              ),
              TextButton(
                onPressed: () {
                  Auth().resetPassword(emailController.text);
                },
                child: const Text('Forgot Password?'),
              ),
              SizedBox(
                width: SizeConfig.blockSizeHorizontal! * 75,
                height: SizeConfig.blockSizeVertical! * 7,
                child: ElevatedButton(
                  style: ElevatedButton.styleFrom(backgroundColor: Colors.blue),
                  onPressed: () {
                    Auth()
                        .signIn(emailController.text, passwordController.text)
                        .then((value) {
                      if (value == null) {
                        return;
                      }
                      Navigator.pushNamed(context, '/home');
                    });
                  },
                  child: const Text('Login',
                      style: TextStyle(color: Colors.white)),
                ),
              ),
              SizedBox(
                width: SizeConfig.blockSizeHorizontal! * 75,
                height: SizeConfig.blockSizeVertical! * 7,
                child: ElevatedButton(
                  style: ElevatedButton.styleFrom(backgroundColor: Colors.red),
                  onPressed: () {
                    Navigator.pushNamed(context, '/signup');
                  },
                  child: const Text('Sign Up',
                      style: TextStyle(color: Colors.white)),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
