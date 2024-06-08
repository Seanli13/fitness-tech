import 'package:flutter/material.dart';
import 'package:mobile_app/services/auth.dart';
import 'package:mobile_app/size_config.dart';
import 'package:url_launcher/url_launcher.dart';

class SignupScreen extends StatelessWidget {
  SignupScreen({super.key});

  TextEditingController emailController = TextEditingController();
  TextEditingController passwordController = TextEditingController();
  TextEditingController nameController = TextEditingController();

  Future<void> _launchUrl(String url) async {
    final Uri _url = Uri.parse(url);

    if (!await launchUrl(_url)) {
      throw Exception('Could not launch $_url');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Sign Up'),
      ),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(18.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.spaceAround,
            children: <Widget>[
              const Text('BlindVision', style: TextStyle(fontSize: 45)),
              // TextField(
              //   controller: nameController,
              //   decoration: const InputDecoration(labelText: 'Name'),
              // ),
              TextField(
                controller: emailController,
                decoration: const InputDecoration(labelText: 'Email'),
              ),
              TextField(
                controller: passwordController,
                obscureText: true,
                decoration: const InputDecoration(labelText: 'Password'),
              ),
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  TextButton(
                    onPressed: () {
                      _launchUrl(
                          'https://doc-hosting.flycricket.io/blindvision-terms-of-use/f777073e-bb66-485f-8634-43df9d876961/terms');
                    },
                    child: const Text('Terms of Service'),
                  ),
                  TextButton(
                    onPressed: () {
                      _launchUrl(
                          'https://doc-hosting.flycricket.io/blindvision-privacy-policy/b8fa562a-fc3a-4d36-9e84-db61722cc4fd/privacy');
                    },
                    child: const Text('Privacy Policy'),
                  ),
                ],
              ),
              SizedBox(
                width: SizeConfig.blockSizeHorizontal! * 75,
                height: SizeConfig.blockSizeVertical! * 7,
                child: ElevatedButton(
                  onPressed: () {
                    Auth()
                        .signUp(emailController.text, passwordController.text,
                            nameController.text)
                        .then((value) {
                      Navigator.pushNamedAndRemoveUntil(
                          context, "/", (route) => false);
                    });
                  },
                  child: const Text('Sign Up'),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
