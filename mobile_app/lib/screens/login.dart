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
              const Text('BlindVision', style: TextStyle(fontSize: 45)),
              TextField(
                controller: emailController,
                decoration: const InputDecoration(labelText: 'Email'),
              ),
              TextField(
                controller: passwordController,
                decoration: const InputDecoration(labelText: 'Password'),
              ),
              SizedBox(
                width: SizeConfig.blockSizeHorizontal! * 75,
                height: SizeConfig.blockSizeVertical! * 7,
                child: ElevatedButton(
                  onPressed: () {
                    Navigator.pushNamed(context, '/signup');
                  },
                  child: const Text('Sign Up'),
                ),
              ),
              SizedBox(
                width: SizeConfig.blockSizeHorizontal! * 75,
                height: SizeConfig.blockSizeVertical! * 7,
                child: ElevatedButton(
                  onPressed: () {
                    Auth()
                        .signIn(emailController.text, passwordController.text)
                        .then((value) {
                      Navigator.pushNamed(context, '/home');
                    });
                  },
                  child: const Text('Login'),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
