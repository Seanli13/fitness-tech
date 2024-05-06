import 'package:flutter/material.dart';
import 'package:mobile_app/services/auth.dart';
import 'package:mobile_app/size_config.dart';

class LoginScreen extends StatelessWidget {
  LoginScreen({super.key});

  TextEditingController emailController = TextEditingController();
  TextEditingController passwordController = TextEditingController();

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
              const Text('FitBlind', style: TextStyle(fontSize: 45)),
              TextField(
                controller: emailController,
                decoration: const InputDecoration(labelText: 'Email'),
              ),
              TextField(
                obscureText: true,
                controller: passwordController,
                decoration: const InputDecoration(labelText: 'Password'),
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
              SizedBox(
                width: SizeConfig.blockSizeHorizontal! * 75,
                height: SizeConfig.blockSizeVertical! * 7,
                child: ElevatedButton(
                  style: ElevatedButton.styleFrom(backgroundColor: Colors.blue),
                  onPressed: () {
                    Auth()
                        .signIn(emailController.text, passwordController.text)
                        .then((value) {
                      Navigator.pushNamed(context, '/home');
                    });
                  },
                  child: const Text('Login',
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