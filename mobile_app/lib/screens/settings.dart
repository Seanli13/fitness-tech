import 'package:flutter/material.dart';
import 'package:mobile_app/services/auth.dart';
import 'package:mobile_app/size_config.dart';
import 'package:url_launcher/url_launcher.dart';

class SettingsScreen extends StatelessWidget {
  const SettingsScreen({super.key});

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
        title: const Text('Settings'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.spaceAround,
          children: <Widget>[
            TextButton(
              onPressed: () {
                _launchUrl(
                    "https://sites.google.com/view/blindvision-fitness/home");
              },
              child: const Text(
                "Go to official website!",
                style: TextStyle(fontSize: 20),
              ),
            ),
            Column(
              children: [
                SizedBox(
                  width: SizeConfig.blockSizeHorizontal! * 75,
                  height: SizeConfig.blockSizeVertical! * 7,
                  child: ElevatedButton(
                    style:
                        ElevatedButton.styleFrom(backgroundColor: Colors.blue),
                    onPressed: () {
                      Auth().signOut().then((value) {
                        Navigator.pushNamedAndRemoveUntil(
                            context, '/', (route) => false);
                      });
                    },
                    child: const Text('Log Out',
                        style: TextStyle(color: Colors.white)),
                  ),
                ),
                SizedBox(
                  height: SizeConfig.blockSizeVertical! * 2,
                ),
                SizedBox(
                  width: SizeConfig.blockSizeHorizontal! * 75,
                  height: SizeConfig.blockSizeVertical! * 7,
                  child: ElevatedButton(
                    style:
                        ElevatedButton.styleFrom(backgroundColor: Colors.red),
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
          ],
        ),
      ),
    );
  }
}
