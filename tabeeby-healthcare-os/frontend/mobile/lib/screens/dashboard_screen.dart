import 'package:flutter/material.dart';

class DashboardScreen extends StatelessWidget {
  const DashboardScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('TABEEBY', style: TextStyle(fontWeight: FontWeight.bold)),
        centerTitle: true,
        backgroundColor: Colors.transparent,
        elevation: 0,
      ),
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
            colors: [Colors.grey[900]!, Colors.blue[900]!, Colors.grey[900]!],
          ),
        ),
        child: SafeArea(
          child: Padding(
            padding: const EdgeInsets.all(16.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text(
                  'Healthcare OS',
                  style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold, color: Colors.cyan),
                ),
                const SizedBox(height: 20),
                Expanded(
                  child: GridView.count(
                    crossAxisCount: 2,
                    crossAxisSpacing: 12,
                    mainAxisSpacing: 12,
                    children: const [
                      FeatureCard(icon: Icons.favorite, label: 'Vitals', color: Colors.red),
                      FeatureCard(icon: Icons.chat_bubble, label: 'AI Physician', color: Colors.green),
                      FeatureCard(icon: Icons.emergency, label: 'Emergency', color: Colors.orange),
                      FeatureCard(icon: Icons.calendar_today, label: 'Appointments', color: Colors.purple),
                      FeatureCard(icon: Icons.medication, label: 'Medications', color: Colors.teal),
                      FeatureCard(icon: Icons.biotech, label: 'Diagnostics', color: Colors.blue),
                    ],
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

class FeatureCard extends StatelessWidget {
  final IconData icon;
  final String label;
  final Color color;
  const FeatureCard({super.key, required this.icon, required this.label, required this.color});

  @override
  Widget build(BuildContext context) {
    return Card(
      color: Colors.white.withOpacity(0.1),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      child: InkWell(
        onTap: () {},
        borderRadius: BorderRadius.circular(16),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(icon, size: 40, color: color),
            const SizedBox(height: 8),
            Text(label, style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w500)),
          ],
        ),
      ),
    );
  }
}
