import 'package:flutter/material.dart';
import 'package:mobile_app/shared/singleton.dart';
import 'package:mobile_app/size_config.dart';

// ignore: must_be_immutable
class ChartScreen extends StatefulWidget {
  ChartScreen({super.key, required this.exerciseType});

  String exerciseType;

  @override
  State<ChartScreen> createState() => _ChartScreenState();
}

class _ChartScreenState extends State<ChartScreen> {
  final Singleton singleton = Singleton();
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
                  ))
            ],
          ),
        ));
  }
}
