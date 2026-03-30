// =========================
// 🔧 COMMON API HELPER
// =========================
async function apiCall(url, method, body = null) {
    try {
        const res = await fetch(url, {
            method: method,
            headers: { "Content-Type": "application/json" },
            body: body ? JSON.stringify(body) : null
        });

        return await res.json();
    } catch (error) {
        console.error("API ERROR:", error);
        return { status: "error", message: "Something went wrong" };
    }
}

// =========================
// 📩 HANDLE ALL FORMS
// =========================
document.addEventListener("submit", async function (e) {

    const form = e.target;
    e.preventDefault();

    const submitBtn = form.querySelector("button[type='submit']");
    if (submitBtn) submitBtn.disabled = true;

    let data = null;

    try {

        // =========================
        // ➕ ADD CLASS
        // =========================
        if (form.id === "addClassForm") {
            const class_name = document.getElementById("className").value.trim();

            if (!class_name) throw "Class name required";

            data = await apiCall("/admin/add-class", "POST", { class_name });
        }

        // =========================
        // ➕ ADD SUBJECT
        // =========================
        else if (form.id === "addSubjectForm") {
            const subject_name = document.getElementById("subjectName").value.trim();

            if (!subject_name) throw "Subject name required";

            data = await apiCall("/admin/add-subject", "POST", { subject_name });
        }

        // =========================
        // ✏️ UPDATE TEACHER
        // =========================
        else if (form.id === "editTeacherForm") {

            const id = document.getElementById("editTeacherId").value;

            data = await apiCall(`/admin/update-teacher/${id}`, "PUT", {
                name: document.getElementById("editName").value,
                email: document.getElementById("editEmail").value,
                phone: document.getElementById("editPhone").value,
                qualification: document.getElementById("editQual").value,
                experience: document.getElementById("editExp").value,
                address: document.getElementById("editAddress").value
            });
        }

        // =========================
        // ➕ ADD TEACHER
        // =========================
        else if (form.id === "addTeacherForm") {

            const name = document.getElementById("teacherName").value.trim();
            const email = document.getElementById("teacherEmail").value.trim();

            if (!name || !email) throw "Name and Email required";

            data = await apiCall("/admin/add-teacher", "POST", {
                name,
                email,
                phone: document.getElementById("teacherPhone").value,
                qualification: document.getElementById("teacherQual").value,
                experience: document.getElementById("teacherExp").value,
                address: document.getElementById("teacherAddress").value
            });
        }

        // =========================
        // ➕ ADD STUDENT
        // =========================
        else if (form.id === "addStudentForm") {

            const name = document.getElementById("studentName").value.trim();
            const email = document.getElementById("studentEmail").value.trim();
            const class_id = document.getElementById("studentClass").value;

            if (!name || !email || !class_id) throw "Name, Email & Class required";

            data = await apiCall("/admin/add-student", "POST", {
                name,
                email,
                class_id,
                age: document.getElementById("studentAge").value,
                gender: document.getElementById("studentGender").value,
                parent_name: document.getElementById("parentName").value,
                parent_phone: document.getElementById("parentPhone").value,
                address: document.getElementById("studentAddress").value
            });
        }

        // =========================
        // ✏️ UPDATE STUDENT
        // =========================

        else if (form.id === "editStudentForm") {

            const id = document.getElementById("editStudentId").value;

            data = await apiCall(`/admin/update-student/${id}`, "PUT", {
                name: document.getElementById("editStudentName").value,
                email: document.getElementById("editStudentEmail").value,
                class_id: document.getElementById("editStudentClass").value,
                age: document.getElementById("editStudentAge").value,
                gender: document.getElementById("editStudentGender").value,
                parent_name: document.getElementById("editParentName").value,
                parent_phone: document.getElementById("editParentPhone").value,
                address: document.getElementById("editStudentAddress").value
            });
        }

        // =========================
        // ✏️ UPDATE CLASS
        // =========================
        else if (form.id === "editClassForm") {

            const id = document.getElementById("editClassId").value;

            data = await apiCall(`/admin/update-class/${id}`, "PUT", {
                class_name: document.getElementById("editClassName").value
            });
        }

        // =========================
        // ✏️ UPDATE SUBJECT
        // =========================
        else if (form.id === "editSubjectForm") {

            const id = document.getElementById("editSubjectId").value;

            data = await apiCall(`/admin/update-subject/${id}`, "PUT", {
                subject_name: document.getElementById("editSubjectName").value
            });
        }

        // =========================
        // ➕ ASSIGN TEACHER
        // =========================
        else if (form.id === "assignTeacherForm") {

            const teacher_id = document.getElementById("assignTeacherId").value;
            const class_id = document.getElementById("assignClassId").value;
            const subject_id = document.getElementById("assignSubjectId").value;

            if (!teacher_id || !class_id || !subject_id) throw "All fields required";

            data = await apiCall("/admin/assign-teacher", "POST", {
                teacher_id,
                class_id,
                subject_id
            });
        }

        // =========================
        // RESPONSE
        // =========================
        if (data) {
            alert(data.message);

            if (data.status === "success") {
                form.reset();
                location.reload();
            }
        }

    } catch (err) {
        alert(err);
    }

    if (submitBtn) submitBtn.disabled = false;
});


// =========================
// 🖱️ HANDLE BUTTON ACTIONS
// =========================
// =========================
// 🖱️ HANDLE BUTTON ACTIONS
// =========================
document.addEventListener("click", async function (e) {

    const target = e.target.closest("button");
    if (!target) return;

    // =========================
    // DELETE
    // =========================
    if (
        target.classList.contains("delete-teacher") ||
        target.classList.contains("delete-student") ||
        target.classList.contains("delete-subject") ||
        target.classList.contains("delete-class")
    ) {
        const id = target.dataset.id;

        let url = "";

        if (target.classList.contains("delete-teacher"))
            url = `/admin/delete-teacher/${id}`;
        else if (target.classList.contains("delete-student"))
            url = `/admin/delete-student/${id}`;
        else if (target.classList.contains("delete-subject"))
            url = `/admin/delete-subject/${id}`;
        else if (target.classList.contains("delete-class"))
            url = `/admin/delete-class/${id}`;

        if (!confirm("Are you sure?")) return;

        const data = await apiCall(url, "DELETE");

        alert(data.message);

        if (data.status === "success") location.reload();
    }

    // =========================
    // 👁 VIEW STUDENT
    // =========================
    if (target.classList.contains("view-student")) {
        const id = target.dataset.id;

        const data = await apiCall(`/admin/get-student/${id}`, "GET");

        document.getElementById("sName").innerText = data.name;
        document.getElementById("sEmail").innerText = data.email;
        document.getElementById("sClass").innerText = data.class;
        document.getElementById("sAge").innerText = data.age;
        document.getElementById("sGender").innerText = data.gender;
        document.getElementById("sParent").innerText = data.parent_name;
        document.getElementById("sPhone").innerText = data.parent_phone;
        document.getElementById("sAddr").innerText = data.address;

        new bootstrap.Modal(document.getElementById("viewStudentModal")).show();
    }

    // =========================
    // 👁 VIEW TEACHER
    // =========================
    if (target.classList.contains("view-teacher")) {
        const id = target.dataset.id;

        const data = await apiCall(`/admin/get-teacher/${id}`, "GET");

        document.getElementById("tName").innerText = data.name;
        document.getElementById("tEmail").innerText = data.email;
        document.getElementById("tPhone").innerText = data.phone;
        document.getElementById("tQual").innerText = data.qualification;
        document.getElementById("tExp").innerText = data.experience;
        document.getElementById("tAddr").innerText = data.address;

        new bootstrap.Modal(document.getElementById("viewTeacherModal")).show();
    }

    // =========================
    // ✏️ EDIT TEACHER (OPEN MODAL)
    // =========================
    if (target.classList.contains("edit-teacher")) {
        const id = target.dataset.id;

        const data = await apiCall(`/admin/get-teacher/${id}`, "GET");

        document.getElementById("editTeacherId").value = id;
        document.getElementById("editName").value = data.name;
        document.getElementById("editEmail").value = data.email;
        document.getElementById("editPhone").value = data.phone;
        document.getElementById("editQual").value = data.qualification;
        document.getElementById("editExp").value = data.experience;
        document.getElementById("editAddress").value = data.address;

        new bootstrap.Modal(document.getElementById("editTeacherModal")).show();
    }

    // =========================
    // ✏️ EDIT CLASS
    // =========================
    if (target.classList.contains("edit-class")) {
        const id = target.dataset.id;

        const data = await apiCall(`/admin/get-class/${id}`, "GET");

        document.getElementById("editClassId").value = id;
        document.getElementById("editClassName").value = data.class_name;

        new bootstrap.Modal(document.getElementById("editClassModal")).show();
    }

    // =========================
    // ✏️ EDIT SUBJECT
    // =========================
    if (target.classList.contains("edit-subject")) {
        const id = target.dataset.id;

        const data = await apiCall(`/admin/get-subject/${id}`, "GET");

        document.getElementById("editSubjectId").value = id;
        document.getElementById("editSubjectName").value = data.subject_name;

        new bootstrap.Modal(document.getElementById("editSubjectModal")).show();
    }

    // =========================
    // ✏️ EDIT STUDENT
    // =========================
    if (target.classList.contains("edit-student")) {
        const id = target.dataset.id;

        const data = await apiCall(`/admin/get-student/${id}`, "GET");

        document.getElementById("editStudentId").value = id;
        document.getElementById("editStudentName").value = data.name;
        document.getElementById("editStudentEmail").value = data.email;
        document.getElementById("editStudentClass").value = String(data.class_id);
        document.getElementById("editStudentAge").value = data.age;
        document.getElementById("editStudentGender").value = data.gender;
        document.getElementById("editParentName").value = data.parent_name;
        document.getElementById("editParentPhone").value = data.parent_phone;
        document.getElementById("editStudentAddress").value = data.address;

        new bootstrap.Modal(document.getElementById("editStudentModal")).show();
    }

    // =========================
    // 👁 VIEW CLASS  ✅ FIXED
    // =========================
    if (target.classList.contains("view-class")) {
        const id = target.dataset.id;

        const data = await apiCall(`/admin/get-class/${id}`, "GET");

        document.getElementById("viewClassName").innerText = data.class_name;

        new bootstrap.Modal(document.getElementById("viewClassModal")).show();
    }

    // =========================
    // 👁 VIEW SUBJECT
    // =========================
    if (target.classList.contains("view-subject")) {
        const id = target.dataset.id;

        const data = await apiCall(`/admin/get-subject/${id}`, "GET");

        document.getElementById("viewSubjectName").innerText = data.subject_name;

        new bootstrap.Modal(document.getElementById("viewSubjectModal")).show();
    }

});