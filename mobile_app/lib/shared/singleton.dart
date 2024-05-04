import 'package:flutter/material.dart';

class Singleton extends ChangeNotifier {
  static final Singleton _singleton = Singleton._internal();

  factory Singleton() {
    return _singleton;
  }

  Singleton._internal();

  String _name = '';

  Map<String, dynamic> userData = {'workouts': []};

  String get name => _name;

  void setName(String name) {
    _name = name;
    notifyListeners();
  }
}
