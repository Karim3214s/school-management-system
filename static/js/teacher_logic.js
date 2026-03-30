document.addEventListener('DOMContentLoaded', () => {
    // 1. Populate and Open Modal
    const modalTriggers = document.querySelectorAll('.marks-modal-trigger');
    modalTriggers.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            // Fill hidden fields for the specific student/subject context [cite: 171]
            document.getElementById('modalStudentId').value = this.dataset.student;
            document.getElementById('modalSubjectId').value = this.dataset.subject;
            document.getElementById('modalAssignmentId').value = this.dataset.assignment;
            document.getElementById('marksInput').value = this.dataset.marks;
            
            // Show the modal using Bootstrap API
            const m = new bootstrap.Modal(document.getElementById('marksModal'));
            m.show();
        });
    });

    // 2. Async Marks Submission 
    const marksForm = document.getElementById('marksForm');
    if (marksForm) {
        marksForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const data = {
                student_id: document.getElementById('modalStudentId').value,
                subject_id: document.getElementById('modalSubjectId').value,
                teacher_assignment_id: document.getElementById('modalAssignmentId').value,
                marks: document.getElementById('marksInput').value
            };

            try {
                const response = await fetch('/teacher/add_marks', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                if (response.ok) {
                    alert("Marks saved!");
                    window.location.reload(); // Refresh to show new marks [cite: 232]
                }
            } catch (err) {
                console.error(err);
                alert("Failed to save marks.");
            }
        });
    }
});