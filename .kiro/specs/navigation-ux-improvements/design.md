# Design Document

## Overview

This design addresses three critical UX issues in the MedMind application's navigation and interaction flows. The solution involves modifying navigation behavior after medication creation, implementing functional "mark as taken" interactions on the dashboard, and ensuring clear medication deletion flows. These changes will create a more intuitive and efficient user experience.

## Architecture

The solution involves modifications to three main areas:

1. **Navigation Flow**: Update the Add Medication Page to navigate to the Dashboard instead of just popping the navigation stack
2. **Dashboard Interactions**: Wire up the verified icon callback in Today's Medications Widget to properly log adherence
3. **Deletion Flow**: Ensure the existing delete functionality is properly connected and add swipe-to-delete as an alternative

### Component Interactions

```
Add Medication Page
  └─> On Success: Navigator.pushNamedAndRemoveUntil('/') 
      └─> Dashboard (via MainLayout bottom nav)

Dashboard
  └─> Today's Medications Widget
      └─> Medication Card (with onTaken callback)
          └─> Dashboard BLoC: LogMedicationTakenEvent
              └─> Adherence BLoC: Log adherence
              └─> PendingDoseTracker: Remove pending dose
              └─> UI: Update progress indicator

Medication List Page
  └─> Swipe gesture on card
      └─> Confirmation dialog
          └─> Medication BLoC: DeleteMedicationRequested
```

## Components and Interfaces

### 1. Add Medication Page Navigation

**Current Behavior:**
- Uses `Navigator.pop(context)` after successful add
- Takes user back to Medication List Page (previous screen)
- No way to return to Dashboard from Medication List

**New Behavior:**
- Use `Navigator.pushNamedAndRemoveUntil(context, '/', (route) => false)` after successful add
- Clears navigation stack and returns to root (Dashboard)
- User can still access Medication List via bottom navigation

### 2. Dashboard Medication Interaction

**Current State:**
- `onTaken` callback is passed to MedicationCard but not wired to BLoC
- Icon button exists but does nothing when clicked

**Required Changes:**
- Dashboard already has `onMedicationTaken` callback that dispatches `LogMedicationTakenEvent`
- This event handler needs to:
  - Create an AdherenceLogEntity
  - Dispatch to AdherenceBloc
  - Call PendingDoseTracker.removePendingDose()
  - Show success snackbar
  - Trigger dashboard refresh to update progress

### 3. Medication Deletion Flow

**Current Implementation:**
- Delete option exists in MedicationDetailPage popup menu
- Shows confirmation dialog
- Dispatches DeleteMedicationRequested event
- Navigates back on success

**Enhancement:**
- Add delete icon button on each medication card in MedicationListPage
- Show confirmation dialog before deletion
- Maintain existing detail page delete option
- More accessible than swipe gestures, especially on laptops

## Data Models

No new data models required. Existing entities are sufficient:

- `MedicationEntity`: Represents medication data
- `AdherenceLogEntity`: Represents adherence log entries
- `DashboardBloc` state: Contains today's medications and adherence stats

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Navigation after add returns to dashboard

*For any* successful medication addition, the navigation stack should be cleared and the user should land on the Dashboard page, and a success message should be displayed.

**Validates: Requirements 1.1, 1.4**

### Property 2: Home navigation always returns to dashboard

*For any* page in the application with bottom navigation visible, tapping the home icon should navigate to the Dashboard.

**Validates: Requirements 1.3**

### Property 3: Mark as taken updates all related state

*For any* medication marked as taken from the dashboard, the system should create an adherence log entry with status "taken", decrement the pending dose count, display visual feedback, and update the progress indicator.

**Validates: Requirements 2.1, 2.2, 2.3, 2.4, 2.5**

### Property 4: Delete requires confirmation

*For any* delete action (from detail page or swipe), a confirmation dialog should be displayed before the medication is removed.

**Validates: Requirements 3.2**

### Property 5: Confirmed deletion removes medication and provides feedback

*For any* confirmed medication deletion, the medication should no longer appear in subsequent queries, the user should be navigated back to the Medication List Page, and a confirmation message should be displayed.

**Validates: Requirements 3.3, 3.4, 3.5**

## Error Handling

### Navigation Errors
- If navigation fails after adding medication, show error snackbar and keep user on current page
- Log navigation errors for debugging

### Adherence Logging Errors
- If adherence log creation fails, show error message to user
- Do not decrement pending dose count if logging fails
- Retry mechanism for transient failures

### Deletion Errors
- If deletion fails, show error message and keep medication in list
- Do not navigate away from current page on deletion failure
- Handle offline scenarios by queuing deletion for later sync

## Testing Strategy

### Unit Tests

1. **Navigation Tests**
   - Test that successful medication add triggers correct navigation
   - Test that navigation clears the stack appropriately
   - Test that bottom navigation home button navigates to dashboard

2. **Dashboard Interaction Tests**
   - Test that onMedicationTaken callback is invoked when icon is tapped
   - Test that adherence log is created with correct data
   - Test that pending dose count is decremented
   - Test that progress indicator updates after marking as taken

3. **Deletion Tests**
   - Test that delete action shows confirmation dialog
   - Test that confirmed deletion removes medication
   - Test that cancelled deletion keeps medication
   - Test swipe-to-delete gesture recognition

### Property-Based Tests

Property-based testing will use the `test` package with custom property test framework already established in the codebase.

1. **Property Test: Navigation Consistency**
   - Generate random medication data
   - Add medication and verify navigation lands on dashboard
   - Verify navigation stack is cleared

2. **Property Test: Adherence Logging**
   - Generate random medications
   - Mark as taken and verify adherence log exists
   - Verify log has correct medication ID and timestamp

3. **Property Test: Deletion Idempotence**
   - Generate random medications
   - Delete medication and verify it's removed
   - Attempt to delete again and verify graceful handling

### Integration Tests

1. **End-to-End Add Flow**
   - Navigate to add medication page
   - Fill form and submit
   - Verify landing on dashboard
   - Verify medication appears in today's list

2. **End-to-End Mark as Taken Flow**
   - Start on dashboard with pending medications
   - Tap verified icon
   - Verify adherence log created
   - Verify pending count decremented
   - Verify progress indicator updated

3. **End-to-End Delete Flow**
   - Navigate to medication detail
   - Trigger delete from menu
   - Confirm deletion
   - Verify navigation to list
   - Verify medication removed

## Implementation Notes

### Navigation Best Practices
- Use named routes for consistency
- Clear navigation stack when returning to root
- Ensure bottom navigation state is preserved

### State Management
- Use BLoC pattern for all state changes
- Ensure proper event dispatching and state listening
- Handle loading and error states appropriately

### UI/UX Considerations
- Provide immediate visual feedback for all actions
- Use snackbars for success/error messages
- Ensure confirmation dialogs are clear and actionable
- Maintain consistent interaction patterns across the app
