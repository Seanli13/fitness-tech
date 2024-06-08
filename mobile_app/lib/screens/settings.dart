import 'package:flutter/material.dart';
import 'package:mobile_app/services/auth.dart';
import 'package:mobile_app/size_config.dart';

class SettingsScreen extends StatelessWidget {
  const SettingsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Settings'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.spaceAround,
          children: <Widget>[
            SizedBox(
              width: SizeConfig.blockSizeHorizontal! * 75,
              height: SizeConfig.blockSizeVertical! * 7,
              child: ElevatedButton(
                style: ElevatedButton.styleFrom(backgroundColor: Colors.blue),
                onPressed: () {
                  Navigator.pushNamed(context, '/login');
                },
                child: const Text('Log Out',
                    style: TextStyle(color: Colors.white)),
              ),
            ),
            SizedBox(
              width: SizeConfig.blockSizeHorizontal! * 75,
              height: SizeConfig.blockSizeVertical! * 7,
              child: ElevatedButton(
                style: ElevatedButton.styleFrom(backgroundColor: Colors.red),
                onPressed: () {
                  Auth().deleteAccount().then((value) {
                    Navigator.pushNamedAndRemoveUntil(
                        context, '/', (route) => false);
                  });
                },
                child: const Text('Delete Account',
                    style: TextStyle(color: Colors.white)),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
