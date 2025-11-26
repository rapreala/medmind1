import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import '../blocs/adherence_bloc/adherence_bloc.dart';
import '../blocs/adherence_bloc/adherence_event.dart';
import '../blocs/adherence_bloc/adherence_state.dart';
import '../widgets/adherence_calendar.dart';
import '../../domain/entities/adherence_log_entity.dart' as entities;
import '../../../../core/widgets/loading_widget.dart';
import '../../../../core/widgets/error_widget.dart';

class AdherenceHistoryPage extends StatefulWidget {
  const AdherenceHistoryPage({super.key});

  @override
  State<AdherenceHistoryPage> createState() => _AdherenceHistoryPageState();
}

class _AdherenceHistoryPageState extends State<AdherenceHistoryPage> {
  DateTime _selectedMonth = DateTime.now();

  @override
  void initState() {
    super.initState();
    _loadAdherenceData();
  }

  void _loadAdherenceData() {
    final startDate = DateTime(_selectedMonth.year, _selectedMonth.month, 1);
    final endDate = DateTime(_selectedMonth.year, _selectedMonth.month + 1, 0);
    
    context.read<AdherenceBloc>().add(
      GetAdherenceLogsRequested(
        startDate: startDate,
        endDate: endDate,
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Adherence History'),
        actions: [
          IconButton(
            icon: const Icon(Icons.analytics_outlined),
            onPressed: () => Navigator.pushNamed(context, '/adherence-analytics'),
          ),
        ],
      ),
      body: Column(
        children: [
          // Month selector
          Container(
            padding: const EdgeInsets.all(16),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                IconButton(
                  onPressed: () => _changeMonth(-1),
                  icon: const Icon(Icons.chevron_left),
                ),
                Text(
                  _getMonthYearString(_selectedMonth),
                  style: Theme.of(context).textTheme.titleMedium?.copyWith(
                    fontWeight: FontWeight.w600,
                  ),
                ),
                IconButton(
                  onPressed: _selectedMonth.isBefore(DateTime.now()) ? () => _changeMonth(1) : null,
                  icon: const Icon(Icons.chevron_right),
                ),
              ],
            ),
          ),
          
          // Calendar and logs
          Expanded(
            child: BlocBuilder<AdherenceBloc, AdherenceState>(
              builder: (context, state) {
                if (state is AdherenceLoading) {
                  return const LoadingWidget();
                }
                
                if (state is AdherenceError) {
                  return ErrorDisplayWidget(
                    message: state.message,
                    onRetry: _loadAdherenceData,
                  );
                }
                
                if (state is AdherenceLogsLoaded) {
                  return SingleChildScrollView(
                    padding: const EdgeInsets.all(16),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        // Calendar view
                        AdherenceCalendar(
                          selectedMonth: _selectedMonth,
                          adherenceLogs: state.logs,
                          onDateSelected: (date) => _showDayDetails(context, date, state.logs),
                        ),
                        const SizedBox(height: 24),
                        
                        // Monthly summary
                        _buildMonthlySummary(context, state.logs),
                        const SizedBox(height: 16),
                        
                        // Recent logs list
                        _buildRecentLogs(context, state.logs),
                      ],
                    ),
                  );
                }
                
                return const SizedBox.shrink();
              },
            ),
          ),
        ],
      ),
    );
  }

  void _changeMonth(int delta) {
    setState(() {
      _selectedMonth = DateTime(_selectedMonth.year, _selectedMonth.month + delta, 1);
    });
    _loadAdherenceData();
  }

  String _getMonthYearString(DateTime date) {
    const months = [
      'January', 'February', 'March', 'April', 'May', 'June',
      'July', 'August', 'September', 'October', 'November', 'December'
    ];
    return '${months[date.month - 1]} ${date.year}';
  }

  Widget _buildMonthlySummary(BuildContext context, List<dynamic> logs) {
    final totalDays = DateTime(_selectedMonth.year, _selectedMonth.month + 1, 0).day;
    final adherentDays = logs.length; // Simplified calculation
    final adherenceRate = (adherentDays / totalDays * 100).round();

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Monthly Summary',
              style: Theme.of(context).textTheme.titleMedium?.copyWith(
                fontWeight: FontWeight.w600,
              ),
            ),
            const SizedBox(height: 12),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceAround,
              children: [
                _buildSummaryItem(context, 'Adherence Rate', '$adherenceRate%'),
                _buildSummaryItem(context, 'Days Tracked', '$adherentDays'),
                _buildSummaryItem(context, 'Missed Days', '${totalDays - adherentDays}'),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildSummaryItem(BuildContext context, String label, String value) {
    return Column(
      children: [
        Text(
          value,
          style: Theme.of(context).textTheme.titleLarge?.copyWith(
            fontWeight: FontWeight.bold,
            color: Theme.of(context).colorScheme.primary,
          ),
        ),
        Text(
          label,
          style: Theme.of(context).textTheme.bodySmall,
          textAlign: TextAlign.center,
        ),
      ],
    );
  }

  Widget _buildRecentLogs(BuildContext context, List<dynamic> logs) {
    if (logs.isEmpty) {
      return const Card(
        child: Padding(
          padding: EdgeInsets.all(16),
          child: Text('No adherence data for this month'),
        ),
      );
    }

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'Recent Activity',
          style: Theme.of(context).textTheme.titleMedium?.copyWith(
            fontWeight: FontWeight.w600,
          ),
        ),
        const SizedBox(height: 8),
        ...logs.take(5).map((log) => ListTile(
          leading: const Icon(Icons.check_circle, color: Colors.green),
          title: Text('Medication taken'),
          subtitle: Text('Today at 8:00 AM'), // Simplified
          trailing: const Icon(Icons.chevron_right),
        )),
      ],
    );
  }

  void _showDayDetails(BuildContext context, DateTime date, List<dynamic> logs) {
    print('📅 Showing details for date: ${date.year}-${date.month}-${date.day}');
    print('📅 Total logs received: ${logs.length}');
    
    // Filter logs for the selected date
    final logsForDay = logs.where((log) {
      if (log is! entities.AdherenceLogEntity) return false;
      final logDate = log.scheduledTime;
      return logDate.year == date.year &&
             logDate.month == date.month &&
             logDate.day == date.day;
    }).cast<entities.AdherenceLogEntity>().toList();
    
    print('📅 Logs for selected day: ${logsForDay.length}');
    
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      builder: (context) => DraggableScrollableSheet(
        initialChildSize: 0.5,
        minChildSize: 0.3,
        maxChildSize: 0.9,
        expand: false,
        builder: (context, scrollController) => Container(
          padding: const EdgeInsets.all(16),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Header
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(
                    'Adherence for ${date.day}/${date.month}/${date.year}',
                    style: Theme.of(context).textTheme.titleMedium?.copyWith(
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                  IconButton(
                    icon: const Icon(Icons.close),
                    onPressed: () => Navigator.pop(context),
                  ),
                ],
              ),
              const SizedBox(height: 16),
              
              // Content
              Expanded(
                child: logsForDay.isEmpty
                  ? const Center(
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Icon(Icons.calendar_today, size: 48, color: Colors.grey),
                          SizedBox(height: 16),
                          Text(
                            'No medications logged for this day',
                            style: TextStyle(color: Colors.grey),
                          ),
                        ],
                      ),
                    )
                  : ListView.builder(
                      controller: scrollController,
                      itemCount: logsForDay.length,
                      itemBuilder: (context, index) {
                        final log = logsForDay[index];
                        return _buildLogItem(context, log);
                      },
                    ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildLogItem(BuildContext context, entities.AdherenceLogEntity log) {
    // Determine icon and color based on status
    IconData icon;
    Color iconColor;
    String statusText;
    
    switch (log.status) {
      case entities.AdherenceStatus.taken:
        icon = Icons.check_circle;
        iconColor = Colors.green;
        statusText = 'Taken';
        break;
      case entities.AdherenceStatus.missed:
        icon = Icons.cancel;
        iconColor = Colors.red;
        statusText = 'Missed';
        break;
      case entities.AdherenceStatus.snoozed:
        icon = Icons.snooze;
        iconColor = Colors.orange;
        statusText = 'Snoozed';
        break;
    }
    
    // Format times
    final scheduledTimeStr = '${log.scheduledTime.hour.toString().padLeft(2, '0')}:${log.scheduledTime.minute.toString().padLeft(2, '0')}';
    final takenTimeStr = log.takenTime != null
        ? '${log.takenTime!.hour.toString().padLeft(2, '0')}:${log.takenTime!.minute.toString().padLeft(2, '0')}'
        : null;
    
    return Card(
      margin: const EdgeInsets.only(bottom: 8),
      child: ListTile(
        leading: Icon(icon, color: iconColor, size: 32),
        title: Text(
          'Medication ID: ${log.medicationId.substring(0, 8)}...',
          style: const TextStyle(fontWeight: FontWeight.w500),
        ),
        subtitle: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const SizedBox(height: 4),
            Text('Status: $statusText'),
            Text('Scheduled: $scheduledTimeStr'),
            if (takenTimeStr != null) Text('Taken at: $takenTimeStr'),
            if (log.snoozeDuration != null) Text('Snoozed for: ${log.snoozeDuration} min'),
          ],
        ),
        isThreeLine: true,
      ),
    );
  }
}