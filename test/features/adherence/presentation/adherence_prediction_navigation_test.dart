import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:medmind/features/adherence/presentation/pages/adherence_prediction_page.dart';

void main() {
  group('Adherence Prediction Navigation Tests', () {
    testWidgets('AdherencePredictionPage can be instantiated and displayed', (
      WidgetTester tester,
    ) async {
      await tester.pumpWidget(
        const MaterialApp(home: AdherencePredictionPage()),
      );

      // Verify that the Adherence Prediction page is displayed
      expect(find.text('Adherence Prediction'), findsOneWidget);
      expect(find.text('Predict Your Adherence Rate'), findsOneWidget);
    });

    testWidgets('Prediction page displays all required input fields', (
      WidgetTester tester,
    ) async {
      await tester.pumpWidget(
        const MaterialApp(home: AdherencePredictionPage()),
      );

      // Verify all 8 input fields are present
      expect(find.text('Age'), findsOneWidget);
      expect(find.text('Number of Medications'), findsOneWidget);
      expect(find.text('Medication Complexity'), findsOneWidget);
      expect(find.text('Days Since Start'), findsOneWidget);
      expect(find.text('Missed Doses Last Week'), findsOneWidget);
      expect(find.text('Snooze Frequency'), findsOneWidget);
      expect(find.text('Chronic Conditions'), findsOneWidget);
      expect(find.text('Previous Adherence Rate'), findsOneWidget);

      // Verify the Predict button is present
      expect(find.text('Predict Adherence'), findsOneWidget);
    });

    testWidgets('Can navigate to AdherencePredictionPage using Navigator', (
      WidgetTester tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            appBar: AppBar(title: const Text('Home')),
            body: Builder(
              builder: (context) => Center(
                child: ElevatedButton(
                  onPressed: () {
                    Navigator.of(context).push(
                      MaterialPageRoute(
                        builder: (context) => const AdherencePredictionPage(),
                      ),
                    );
                  },
                  child: const Text('Go to Prediction'),
                ),
              ),
            ),
          ),
        ),
      );

      // Verify we're on the home page
      expect(find.text('Home'), findsOneWidget);
      expect(find.text('Go to Prediction'), findsOneWidget);

      // Navigate to prediction page
      await tester.tap(find.text('Go to Prediction'));
      await tester.pumpAndSettle();

      // Verify that we're now on the Adherence Prediction page
      expect(find.text('Adherence Prediction'), findsOneWidget);
      expect(find.text('Predict Your Adherence Rate'), findsOneWidget);
    });

    testWidgets('Can navigate back from AdherencePredictionPage', (
      WidgetTester tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            appBar: AppBar(title: const Text('Home')),
            body: Builder(
              builder: (context) => Center(
                child: ElevatedButton(
                  onPressed: () {
                    Navigator.of(context).push(
                      MaterialPageRoute(
                        builder: (context) => const AdherencePredictionPage(),
                      ),
                    );
                  },
                  child: const Text('Go to Prediction'),
                ),
              ),
            ),
          ),
        ),
      );

      // Navigate to prediction page
      await tester.tap(find.text('Go to Prediction'));
      await tester.pumpAndSettle();

      // Verify we're on the prediction page
      expect(find.text('Adherence Prediction'), findsOneWidget);

      // Navigate back
      await tester.tap(find.byType(BackButton));
      await tester.pumpAndSettle();

      // Verify we're back on the home page
      expect(find.text('Home'), findsOneWidget);
      expect(find.text('Go to Prediction'), findsOneWidget);
    });

    testWidgets('Prediction page has proper AppBar with title', (
      WidgetTester tester,
    ) async {
      await tester.pumpWidget(
        const MaterialApp(home: AdherencePredictionPage()),
      );

      // Verify AppBar exists with correct title
      expect(
        find.widgetWithText(AppBar, 'Adherence Prediction'),
        findsOneWidget,
      );
    });
  });
}
