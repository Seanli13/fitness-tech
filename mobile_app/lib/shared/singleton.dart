import 'package:flutter/material.dart';

class Singleton extends ChangeNotifier {
  static final Singleton _singleton = Singleton._internal();

  factory Singleton() {
    return _singleton;
  }

  Singleton._internal();

  String _name = '';

  Map<String, dynamic> userData = {'workouts': {}};

  String get name => _name;

  final dataNameToName = {
    "bicep_curl": "Bicep Curls",
    "pushups": "Pushups",
    "downward_dog": "Downward Dog",
    "plank": "Plank",
    "squats": "Squats",
    "bench_press": "Bench Press",
    "deadlift": "Deadlift",
  };

  void setName(String name) {
    _name = name;
    notifyListeners();
  }
}
