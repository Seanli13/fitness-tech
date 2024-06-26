import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';
import 'package:mobile_app/shared/singleton.dart';
import 'package:mobile_app/size_config.dart';
import 'package:syncfusion_flutter_charts/charts.dart';

class ChartData {
  ChartData(this.x, this.y);
  final DateTime x;
  final double y;
}

// ignore: must_be_immutable
class ChartScreen extends StatefulWidget {
  ChartScreen({super.key, required this.exerciseType});

  String exerciseType;

  @override
  State<ChartScreen> createState() => _ChartScreenState();
}

class _ChartScreenState extends State<ChartScreen> {
  final Singleton singleton = Singleton();

  List<ChartData> getChartData() {
    List<ChartData> chartData = [];
    // print(singleton.userData['workouts'].entries);
    // List<Map<String, dynamic>> workouts =
    //     List<Map<String, dynamic>>.from(singleton.userData['workouts']);
    for (var workout in singleton.userData['workouts'].entries) {
      if (workout.value['type'] == widget.exerciseType) {
        String millisecondsSinceEpoch = workout.key;
        DateTime date = DateTime.fromMillisecondsSinceEpoch(
            int.parse(millisecondsSinceEpoch));

        chartData.add(ChartData(date, workout.value['reps'] * 1.0));
      }
    }

    // sort the data by date
    chartData.sort((a, b) => a.x.compareTo(b.x));

    return chartData;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          title: Text(singleton.dataNameToName[widget.exerciseType]!),
        ),
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.spaceAround,
            children: <Widget>[
              SizedBox(
                  width: SizeConfig.blockSizeHorizontal! * 90,
                  height: SizeConfig.blockSizeVertical! * 70,
                  child: Card(
                    color: Colors.blue,
                    child: Padding(
                      padding: const EdgeInsets.all(8.0),
                      child: SfCartesianChart(
                        backgroundColor: Colors.black,
                        primaryYAxis: const NumericAxis(
                            labelStyle: TextStyle(color: Colors.white),
                            title: AxisTitle(
                                text: 'Reps',
                                textStyle: TextStyle(color: Colors.white))),
                        primaryXAxis: const DateTimeAxis(
                          labelStyle: TextStyle(color: Colors.white),
                          title: AxisTitle(
                              text: 'Date',
                              textStyle: TextStyle(color: Colors.white)),
                        ),
                        series: <LineSeries<ChartData, DateTime>>[
                          LineSeries<ChartData, DateTime>(
                              dataSource: getChartData(),
                              xValueMapper: (ChartData reps, _) => reps.x,
                              yValueMapper: (ChartData reps, _) => reps.y,
                              name: 'Reps',
                              dataLabelSettings:
                                  DataLabelSettings(isVisible: true))
                        ],
                      ),
                    ),
                  ))
            ],
          ),
        ));
  }
}
