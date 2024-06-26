import 'dart:io';
import 'package:health/health.dart';
import 'package:permission_handler/permission_handler.dart';
import 'package:mobile_app/services/auth.dart';

class HealthUtil {
  final Health _health = Health();

  HealthUtil() {
    _health.configure(useHealthConnectIfAvailable: true);
  }

  List<HealthDataType> get dataTypesIOS => [
        HealthDataType.ACTIVE_ENERGY_BURNED,
        HealthDataType.BASAL_ENERGY_BURNED,
      ];

  List<HealthDataType> get dataTypesAndroid => [
        HealthDataType.ACTIVE_ENERGY_BURNED,
        HealthDataType.BASAL_ENERGY_BURNED,
      ];

  List<HealthDataType> get types =>
      Platform.isIOS ? dataTypesIOS : dataTypesAndroid;

  List<HealthDataAccess> get permissions =>
      types.map((type) => HealthDataAccess.READ).toList();

  Future<void> requestPermissions() async {
    final status = await Permission.activityRecognition.request();
    if (status.isGranted) {
      await _health.requestAuthorization(types, permissions: permissions);
    }
  }

  // get health data ever since date of account creation
  Future<List<HealthDataPoint>> getHealthData() async {
    final user = Auth().user;
    final accountCreationDate = user?.metadata.creationTime;
    final now = DateTime.now();

    List<HealthDataPoint> healthDataList = [];

    try {
      List<HealthDataPoint> healthData = await _health.getHealthDataFromTypes(
        types: types,
        startTime: accountCreationDate!,
        endTime: now,
      );
      healthDataList = _health.removeDuplicates(healthData);
    } catch (e) {
      print(e);
    }

    return healthDataList;
  }

  Future<void> revokeAccess() async {
    await _health.revokePermissions();
  }
}
