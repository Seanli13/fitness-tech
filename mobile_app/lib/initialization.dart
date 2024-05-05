import 'package:flutter/material.dart';
import 'package:mobile_app/shared/singleton.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:mobile_app/services/auth.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'screens/home.dart';
import 'screens/login.dart';

class Initialization extends StatelessWidget {
  const Initialization({super.key});

  @override
  Widget build(BuildContext context) {
    final Singleton singleton = Singleton();
    User? user = Auth().user;
    if (user == null) {
      return LoginScreen();
    }

    return StreamBuilder(
      stream: FirebaseFirestore.instance
          .collection('users')
          .doc(user!.uid)
          .snapshots(),
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          return const CircularProgressIndicator();
        }

        print(snapshot.data);
        if (snapshot.hasData) {
          singleton.userData = snapshot.data!.data() as Map<String, dynamic>;
          print(singleton.userData);
        }
        return const HomeScreen();
      },
    );
  }
}
