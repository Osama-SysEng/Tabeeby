import 'package:flutter/material.dart';
import 'screens/dashboard_screen.dart';

void main() {
  runApp(const TabeebyApp());
}

class TabeebyApp extends StatelessWidget {
  const TabeebyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'TABEEBY',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFF00BCD4),
          brightness: Brightness.dark,
        ),
        useMaterial3: true,
      ),
      home: const DashboardScreen(),
    );
  }
}
