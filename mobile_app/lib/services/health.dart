// import 'dart:io';
// import 'package:health/health.dart';
// import 'package:permission_handler/permission_handler.dart';
// import 'package:mobile_app/services/auth.dart';

// class HealthUtil {
//   final Health _health = Health();

//   HealthUtil() {
//     _health.configure(useHealthConnectIfAvailable: true);
//   }

//   List<HealthDataType> get dataTypesIOS => [
//         HealthDataType.ACTIVE_ENERGY_BURNED,
//         HealthDataType.BASAL_ENERGY_BURNED,
//       ];

//   List<HealthDataType> get dataTypesAndroid => [
//         HealthDataType.ACTIVE_ENERGY_BURNED,
//         HealthDataType.BASAL_ENERGY_BURNED,
//       ];

//   List<HealthDataType> get types => (Platform.isAndroid)
//       ? dataTypesAndroid
//       : (Platform.isIOS)
//           ? dataTypesIOS
//           : [];

//   List<HealthDataAccess> get permissions =>
//       types.map((e) => HealthDataAccess.READ).toList();

//   Future<bool> authorize() async {
//     await Permission.activityRecognition.request();
//     await Permission.location.request();

//     bool? hasPermissions =
//         await _health.hasPermissions(types, permissions: permissions);

//     print("Has permissions: $hasPermissions");

//     hasPermissions ??= false;

//     bool authorized = false;
//     if (!hasPermissions) {
//       try {
//         print(
//             "Requesting authorization for types: $types and permissions: $permissions");
//         authorized =
//             await _health.requestAuthorization(types, permissions: permissions);
//         print("Authorization status: $authorized");
//       } catch (error) {
//         print("Exception in authorize: $error");
//       }
//     }
//     return authorized;
//   }

//   // get health data ever since date of account creation
//   Future<List<HealthDataPoint>> getHealthData() async {
//     final user = Auth().user;
//     final accountCreationDate = user?.metadata.creationTime;
//     final now = DateTime.now();

//     List<HealthDataPoint> healthDataList = [];

//     try {
//       List<HealthDataPoint> healthData = await _health.getHealthDataFromTypes(
//         types: types,
//         startTime: accountCreationDate!,
//         endTime: now,
//       );
//       healthDataList = _health.removeDuplicates(healthData);
//     } catch (e) {
//       print(e);
//     }

//     return healthDataList;
//   }

//   Future<void> revokeAccess() async {
//     await _health.revokePermissions();
//   }
// }
