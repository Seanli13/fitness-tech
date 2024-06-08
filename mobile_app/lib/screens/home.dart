import 'package:flutter/material.dart';
import 'package:mobile_app/shared/singleton.dart';
import 'package:mobile_app/services/auth.dart';
import 'package:mobile_app/size_config.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

final dataNameToName = {
  "bicep_curl": "Bicep Curls",
  "pushups": "Pushups",
  "downward_dog": "Downward Dog",
  "plank": "Plank",
  "squats": "Squats",
  "bench_press": "Bench Press",
  "deadlift": "Deadlift",
};

class _HomeScreenState extends State<HomeScreen> {
  final Singleton singleton = Singleton();
  List<Map<String, dynamic>> workouts = [];
  List<Map<String, dynamic>> records = [];

  String timestampToTime(int timestamp) {
    var date = DateTime.fromMillisecondsSinceEpoch(timestamp);
    return "${date.month}/${date.day}/${date.year} ${date.hour}:${date.minute}";
  }

  List<Map<String, dynamic>> getWorkouts() {
    if (singleton.userData['workouts'] == null) {
      return [];
    }
    print(singleton.userData['workouts']);

    List<Map<String, dynamic>> workouts = [];

    if (singleton.userData['workouts'].isEmpty) {
      return [];
    }
    for (var time in singleton.userData['workouts'].keys) {
      var workout = singleton.userData['workouts'][time];
      workout['time'] = timestampToTime(int.parse(time));
      workouts.add(workout);
    }

    return workouts;
  }

  List<Map<String, dynamic>> getRecords() {
    if (singleton.userData['records'] == null) {
      return [];
    }

    List<Map<String, dynamic>> records = [];

    for (var workout in singleton.userData['records'].keys) {
      records.add({workout: singleton.userData['records'][workout]});
    }

    return records;
  }

  int getRecord(String workout) {
    if (singleton.userData['records'] == null) {
      return 0;
    }

    return singleton.userData['records'][workout];
  }

  @override
  Widget build(BuildContext context) {
    workouts = getWorkouts();
    records = getRecords();

    return Scaffold(
        appBar: AppBar(
          centerTitle: true,
          title: Text((Auth().user != null) ? Auth().user!.displayName! : "",
              style:
                  const TextStyle(fontSize: 25, fontWeight: FontWeight.bold)),
          actions: [
            IconButton(
              icon: const Icon(Icons.settings),
              onPressed: () {
                Navigator.pushNamed(context, '/settings');
              },
            )
          ],
        ),
        body: SizedBox(
            width: SizeConfig.blockSizeHorizontal! * 100,
            height: SizeConfig.blockSizeVertical! * 100,
            child: ListView.builder(
              itemCount: (singleton.userData["workouts"] != null)
                  ? singleton.userData['workouts'].length
                  : 0,
              itemBuilder: (context, index) {
                return Padding(
                  padding: const EdgeInsets.all(8.0),
                  child: ListTile(
                    tileColor: Colors.blue,
                    title: Text(
                        "${dataNameToName[workouts[index]['type']]!} - ${workouts[index]['time']}",
                        style:
                            const TextStyle(color: Colors.white, fontSize: 25)),
                    subtitle: Text(
                      "Reps: ${workouts[index]['reps'].toString()}\nHighest: ${getRecord(workouts[index]['type']).toString()}",
                      style: const TextStyle(color: Colors.white),
                    ),
                  ),
                );
              },
            )));
  }
}
