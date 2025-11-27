# Implementation Plan

- [x] 1. Fix navigation after adding medication
  - [x] 1.1 Update Add Medication Page navigation logic
    - Modify the BlocListener in AddMedicationPage to use `Navigator.pushNamedAndRemoveUntil(context, '/', (route) => false)` instead of `Navigator.pop(context)`
    - Ensure this applies to both add and edit flows (only change add flow)
    - Test that navigation clears the stack and lands on dashboard
    - _Requirements: 1.1, 1.4_

  - [x] 1.2 Write property test for navigation after add
    - **Property 1: Navigation after add returns to dashboard**
    - **Validates: Requirements 1.1, 1.4**

- [-] 2. Implement functional "mark as taken" on dashboard
  - [x] 2.1 Wire up dashboard medication taken callback
    - Update the `LogMedicationTakenEvent` handler in DashboardBloc
    - Create AdherenceLogEntity with current timestamp and "taken" status
    - Dispatch to AdherenceBloc to log adherence
    - Call PendingDoseTracker.removePendingDose() to decrement badge count
    - Trigger dashboard data reload to update progress indicator
    - Show success snackbar with medication name
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5_

  - [x] 2.2 Write property test for mark as taken
    - **Property 3: Mark as taken updates all related state**
    - **Validates: Requirements 2.1, 2.2, 2.3, 2.4, 2.5**

- [x] 3. Add delete button to medication list cards
  - [x] 3.1 Add delete icon button to Medication List Page cards
    - Modify MedicationCard to accept an optional onDelete callback
    - In MedicationListPage, pass onDelete callback that shows confirmation dialog
    - On confirmation, dispatch DeleteMedicationRequested event
    - Add IconButton with delete icon (Icons.delete_outline) to the card
    - Position delete button on the right side of the card (before chevron)
    - _Requirements: 3.2, 3.6_

  - [x] 3.2 Write property test for delete confirmation
    - **Property 4: Delete requires confirmation**
    - **Validates: Requirements 3.2**

  - [x] 3.3 Write property test for deletion completion
    - **Property 5: Confirmed deletion removes medication and provides feedback**
    - **Validates: Requirements 3.3, 3.4, 3.5**

- [x] 4. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.
