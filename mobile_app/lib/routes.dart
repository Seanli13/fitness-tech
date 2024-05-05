import "initialization.dart";
import "screens/home.dart";
import "screens/login.dart";
import "screens/signup.dart";
import 'screens/settings.dart';

var routes = {
  "/": (context) => const Initialization(),
  "/home": (context) => const HomeScreen(),
  "/login": (context) => LoginScreen(),
  "/signup": (context) => SignupScreen(),
  "/settings": (context) => const SettingsScreen(),
};
