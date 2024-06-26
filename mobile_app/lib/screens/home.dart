import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';
import 'package:health/health.dart';
import 'package:mobile_app/shared/singleton.dart';
import 'package:mobile_app/services/auth.dart';
import 'package:mobile_app/size_config.dart';
import 'package:mobile_app/screens/charts.dart';
import 'package:syncfusion_flutter_charts/charts.dart';
import 'package:mobile_app/services/health.dart';

class ChartData {
  ChartData(this.x, this.y, [this.color]);
  final String x;
  final double y;
  final Color? color;
}

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

class _HomeScreenState extends State<HomeScreen> with TickerProviderStateMixin {
  final Singleton singleton = Singleton();
  List<Map<String, dynamic>> workouts = [];
  List<Map<String, dynamic>> records = [];
  late PageController _pageController;
  late TabController _tabController;
  int _currentIndex = 0;

  List<ChartData> chartData = [
    ChartData("bicep_curl", 10),
    ChartData("pushups", 20),
    ChartData("downward_dog", 30),
    ChartData("plank", 40),
  ];

  List<ChartData> updateChartData() {
    List<ChartData> chartData = [];
    Map<String, int> workoutCount = {"bicep_curl": 0};

    if (singleton.userData["workouts"].length > 0) {
      for (var workout in singleton.userData["workouts"].values) {
        // print(workout);
        String workoutName = workout["type"];
        // print(workoutName);

        if (workoutCount.containsKey(workoutName)) {
          workoutCount[workoutName] = workoutCount[workoutName]! + 1;
        } else {
          workoutCount[workoutName] = 1;
        }
      }
    }

    // print(workoutCount);

    for (var workout in workoutCount.keys) {
      chartData.add(ChartData(singleton.dataNameToName[workout]!,
          workoutCount[workout]!.toDouble()));
    }

    return chartData;
  }

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

  Future<void> getHealthData() async {
    HealthUtil healthUtil = HealthUtil();
    print("Requesting Permissions...");
    await healthUtil.requestPermissions();
    print("Getting Health Data...");
    List<HealthDataPoint> healthData = await healthUtil.getHealthData();
    print(healthData);
  }

  @override
  void initState() {
    super.initState();
    _pageController = PageController();
    _tabController = TabController(length: 3, vsync: this);

    getHealthData();
  }

  @override
  void dispose() {
    _pageController.dispose();
    _tabController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    workouts = getWorkouts();
    records = getRecords();
    chartData = updateChartData();

    return Scaffold(
        appBar: AppBar(
          centerTitle: true,
          title: Text(
              // (true/false) ? true : false
              (Auth().user != null && Auth().user!.displayName != null)
                  ? Auth().user!.displayName!
                  : "",
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
        body: Stack(children: [
          SizedBox(
            child: PageView(
                controller: _pageController,
                onPageChanged: (index) {
                  setState(() {
                    _currentIndex = index;
                  });
                },
                children: [
                  Column(
                    children: [
                      SizedBox(
                          width: SizeConfig.blockSizeHorizontal! * 100,
                          height: SizeConfig.blockSizeVertical! * 50,
                          child: ListView.builder(
                            itemCount: (singleton.userData["workouts"] != null)
                                ? singleton.userData['workouts'].length
                                : 0,
                            itemBuilder: (context, index) {
                              return Padding(
                                  padding: const EdgeInsets.all(8.0),
                                  child: FitnessCard(
                                      workoutName: workouts[index]['type']!,
                                      time: "${workouts[index]['time']}",
                                      reps: workouts[index]['reps']));
                            },
                          )),
                      SizedBox(
                        width: SizeConfig.blockSizeHorizontal! * 96,
                        height: SizeConfig.blockSizeVertical! * 30,
                        child: Card(
                            color: Colors.blue,
                            child: Padding(
                              padding: const EdgeInsets.all(8.0),
                              child: SfCircularChart(series: <CircularSeries>[
                                PieSeries<ChartData, String>(
                                  dataSource: chartData,
                                  pointColorMapper: (ChartData data, _) =>
                                      data.color,
                                  xValueMapper: (ChartData data, _) => data.x,
                                  yValueMapper: (ChartData data, _) => data.y,
                                  dataLabelMapper: (ChartData data, _) =>
                                      data.x,
                                  dataLabelSettings: const DataLabelSettings(
                                      textStyle: TextStyle(
                                          color: Colors.white,
                                          fontWeight: FontWeight.bold),
                                      isVisible: true,
                                      labelPosition:
                                          ChartDataLabelPosition.outside),
                                )
                              ]),
                            )),
                      )
                    ],
                  ),
                  Column(
                    children: [
                      Row(
                          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            HealthDataCard(
                              name: "Active Calories",
                              value: 100,
                              unit: "kcal",
                            ),
                            HealthDataCard(
                              name: "Basal Calories",
                              value: 200,
                              unit: "kcal",
                            ),
                          ]),
                    ],
                  ),
                ]),
          ),
        ]));
  }
}

class FitnessCard extends StatelessWidget {
  FitnessCard(
      {super.key,
      required this.workoutName,
      required this.time,
      required this.reps});
  final String workoutName;
  final String time;
  final int reps;

  Singleton singleton = Singleton();

  int getRecord(String workout) {
    if (singleton.userData['records'] == null) {
      return 0;
    }

    return singleton.userData['records'][workout];
  }

  @override
  Widget build(BuildContext context) {
    return Card(
      color: Colors.blue,
      child: InkWell(
        onTap: () {
          Navigator.push(
              context,
              MaterialPageRoute(
                  builder: (context) => ChartScreen(
                        exerciseType: workoutName,
                      )));
        },
        child: Padding(
          padding: const EdgeInsets.all(8.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text("${singleton.dataNameToName[workoutName]} - ${time}",
                  style: const TextStyle(color: Colors.white, fontSize: 25)),
              Text(
                "Reps: ${reps.toString()}\nHighest: ${getRecord(workoutName).toString()}",
                style: const TextStyle(color: Colors.white),
              )
            ],
          ),
        ),
      ),
    );
  }
}

class HealthDataCard extends StatelessWidget {
  const HealthDataCard(
      {super.key, required this.name, required this.value, required this.unit});
  final String name;
  final int value;
  final String unit;

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: SizeConfig.blockSizeHorizontal! * 40,
      height: SizeConfig.blockSizeVertical! * 25,
      child: Card(
        child: Padding(
          padding: const EdgeInsets.all(8.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(name,
                  style: const TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                      color: Colors.orange)),
              Row(
                crossAxisAlignment: CrossAxisAlignment.end,
                children: [
                  Text(value.toString(),
                      style: const TextStyle(
                          fontSize: 20, fontWeight: FontWeight.bold)),
                  Text(" $unit"),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}
