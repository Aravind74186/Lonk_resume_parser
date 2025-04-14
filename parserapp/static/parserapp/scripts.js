// document.addEventListener('DOMContentLoaded', function() {
//   // DRAG & DROP / UPLOAD PAGE FUNCTIONALITY
//   const dropArea = document.getElementById('drop-area');
//   const fileInput = document.getElementById('fileElem');
//   const fileList = document.getElementById('file-list');
//   const uploadForm = document.getElementById('uploadForm');
//   const loader = document.getElementById('loader');

//   if (dropArea) {
//     ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
//       dropArea.addEventListener(eventName, preventDefaults, false);
//       document.body.addEventListener(eventName, preventDefaults, false);
//     });

//     function preventDefaults(e) {
//       e.preventDefault();
//       e.stopPropagation();
//     }

//     ['dragenter', 'dragover'].forEach(eventName => {
//       dropArea.addEventListener(eventName, () => dropArea.classList.add('highlight'), false);
//     });
//     ['dragleave', 'drop'].forEach(eventName => {
//       dropArea.addEventListener(eventName, () => dropArea.classList.remove('highlight'), false);
//     });

//     dropArea.addEventListener('drop', handleDrop, false);

//     function handleDrop(e) {
//       let dt = e.dataTransfer;
//       let files = dt.files;
//       if (fileInput) {
//         fileInput.files = files;
//         displayFileList(files);
//       }
//     }

//     if (fileInput) {
//       fileInput.addEventListener('change', () => {
//         displayFileList(fileInput.files);
//       });
//     }

//     function displayFileList(files) {
//       let list = '';
//       for (let i = 0; i < files.length; i++) {
//         list += `<p>${files[i].name}</p>`;
//       }
//       if (fileList) {
//         fileList.innerHTML = list;
//       }
//     }
//   }

//   if (uploadForm && loader) {
//     uploadForm.addEventListener('submit', function() {
//       loader.style.display = 'flex';
//     });
//   }

//   // MODAL POPUP FUNCTIONALITY FOR RESULTS PAGE USING BOOTSTRAP MODAL API
//   const candidateModalEl = document.getElementById('candidateModal');
//   const candidateDetailsDiv = document.getElementById('candidateDetails');
//   let candidateModalInstance = null;

//   window.showCandidateModal = function(el) {
//     const dataAttr = el.getAttribute('data-result');
//     console.log("Data attribute:", dataAttr);
//     let candidate;
//     try {
//       candidate = JSON.parse(dataAttr);
//     } catch (err) {
//       console.error("Invalid JSON data:", dataAttr, err);
//       if (candidateDetailsDiv) {
//         candidateDetailsDiv.innerHTML = "<p class='text-danger'>Error: Could not load candidate details.</p>";
//       }
//       return;
//     }
//     console.log("Parsed candidate:", candidate);
//     let detailsHtml = `
//       <div class="candidate-info">
//         <p><strong>Name:</strong> ${candidate.personalDetails?.name || ''}</p>
//         <p><strong>Email:</strong> ${Array.isArray(candidate.personalDetails?.contactInfo?.email)
//             ? candidate.personalDetails.contactInfo.email.join(", ")
//             : candidate.personalDetails?.contactInfo?.email || ''}</p>
//         <p><strong>Phone:</strong> ${Array.isArray(candidate.personalDetails?.contactInfo?.phone)
//             ? candidate.personalDetails.contactInfo.phone.join(", ")
//             : candidate.personalDetails?.contactInfo?.phone || ''}</p>
//         <p><strong>Summary:</strong> ${candidate.personalDetails?.summary || ''}</p>
//         <p><strong>Experience:</strong> ${candidate.experience || 'N/A'}</p>
//         <p><strong>Created Date:</strong> ${candidate.created_date || ''}</p>
//         <p><strong>Last Track Time:</strong> ${candidate.last_track_time || ''}</p>
//         <p><strong>Current City:</strong> ${candidate.current_city || 'N/A'}</p>
//       </div>
//     `;
//     if (candidate.education && candidate.education.length) {
//       detailsHtml += `<h3 class="mt-3">Education</h3><ul>`;
//       candidate.education.forEach(edu => {
//         detailsHtml += `<li><strong>${edu.institution || ''}</strong>, ${edu.degree || ''}, ${edu.fieldOfStudy || ''}, ${edu.graduationDate || ''}</li>`;
//       });
//       detailsHtml += `</ul>`;
//     }
//     if (candidate.workExperience && candidate.workExperience.length) {
//       detailsHtml += `<h3 class="mt-3">Work Experience</h3>`;
//       candidate.workExperience.forEach(exp => {
//         detailsHtml += `
//           <div class="mb-2">
//             <p><strong>Company:</strong> ${exp.company || ''}</p>
//             <p><strong>Title:</strong> ${exp.position || exp.title || ''}</p>
//             <p><strong>Duration:</strong> ${exp.employmentDuration || exp.duration || ''}</p>
//             <p><strong>Contributions:</strong> ${exp.notableContributions || ''}</p>
//           </div>
//         `;
//       });
//     }
//     if (candidateDetailsDiv) {
//       candidateDetailsDiv.innerHTML = detailsHtml;
//     }
//     if (candidateModalEl) {
//       if (!candidateModalInstance) {
//         candidateModalInstance = new bootstrap.Modal(candidateModalEl, {
//           keyboard: true
//         });
//       }
//       candidateModalInstance.show();
//     }
//   };

//   window.closeCandidateModal = function() {
//     if (candidateModalEl && candidateModalInstance) {
//       candidateModalInstance.hide();
//     }
//   };

//   window.checkAll = function() {
//     const selectAllCheckbox = document.getElementById('select-all');
//     const checkboxes = document.getElementsByName('select_candidate');
//     for (let i = 0; i < checkboxes.length; i++) {
//       checkboxes[i].checked = selectAllCheckbox.checked;
//     }
//   };
// });
document.addEventListener('DOMContentLoaded', function() {
  // DRAG & DROP / UPLOAD PAGE FUNCTIONALITY
  const dropArea = document.getElementById('drop-area');
  const fileInput = document.getElementById('fileElem');
  const fileList = document.getElementById('file-list');
  const uploadForm = document.getElementById('uploadForm');
  const loader = document.getElementById('loader');

  if (dropArea) {
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
      dropArea.addEventListener(eventName, preventDefaults, false);
      document.body.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
      e.preventDefault();
      e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
      dropArea.addEventListener(eventName, () => dropArea.classList.add('highlight'), false);
    });
    ['dragleave', 'drop'].forEach(eventName => {
      dropArea.addEventListener(eventName, () => dropArea.classList.remove('highlight'), false);
    });

    dropArea.addEventListener('drop', handleDrop, false);

    function handleDrop(e) {
      let dt = e.dataTransfer;
      let files = dt.files;
      if (fileInput) {
        fileInput.files = files;
        displayFileList(files);
      }
    }

    if (fileInput) {
      fileInput.addEventListener('change', () => {
        displayFileList(fileInput.files);
      });
    }

    function displayFileList(files) {
      let list = '';
      for (let i = 0; i < files.length; i++) {
        list += `<p>${files[i].name}</p>`;
      }
      if (fileList) {
        fileList.innerHTML = list;
      }
    }
  }

  if (uploadForm && loader) {
    uploadForm.addEventListener('submit', function() {
      loader.style.display = 'block';
    });
  }

  // MODAL POPUP FUNCTIONALITY FOR RESULTS PAGE USING BOOTSTRAP MODAL API
  const candidateModalEl = document.getElementById('candidateModal');
  const candidateDetailsDiv = document.getElementById('candidateDetails');
  let candidateModalInstance = null;

  window.showCandidateModal = function(el) {
    const dataAttr = el.getAttribute('data-result');
    console.log("Data attribute:", dataAttr);
    let candidate;
    try {
      candidate = JSON.parse(dataAttr);
    } catch (err) {
      console.error("Invalid JSON data:", dataAttr, err);
      if (candidateDetailsDiv) {
        candidateDetailsDiv.innerHTML = "<p class='text-danger'>Error: Could not load candidate details.</p>";
      }
      return;
    }
    console.log("Parsed candidate:", candidate);
    let detailsHtml = `
      <div class="candidate-info">
        <p><strong>Name:</strong> ${candidate.personalDetails?.name || ''}</p>
        <p><strong>Email:</strong> ${Array.isArray(candidate.personalDetails?.contactInfo?.email)
            ? candidate.personalDetails.contactInfo.email.join(", ")
            : candidate.personalDetails?.contactInfo?.email || ''}</p>
        <p><strong>Phone:</strong> ${Array.isArray(candidate.personalDetails?.contactInfo?.phone)
            ? candidate.personalDetails.contactInfo.phone.join(", ")
            : candidate.personalDetails?.contactInfo?.phone || ''}</p>
        <p><strong>Summary:</strong> ${candidate.personalDetails?.summary || ''}</p>
        <p><strong>Experience:</strong> ${candidate.experience || 'N/A'}</p>
        <p><strong>Created Date:</strong> ${candidate.created_date || ''}</p>
        <p><strong>Last Track Time:</strong> ${candidate.last_track_time || ''}</p>
        <p><strong>Current City:</strong> ${candidate.current_city || 'N/A'}</p>
      </div>
    `;
    if (candidate.education && candidate.education.length) {
      detailsHtml += `<h3 class="mt-3">Education</h3><ul>`;
      candidate.education.forEach(edu => {
        detailsHtml += `<li><strong>${edu.institution || ''}</strong>, ${edu.degree || ''}, ${edu.fieldOfStudy || ''}, ${edu.graduationDate || ''}</li>`;
      });
      detailsHtml += `</ul>`;
    }
    if (candidate.workExperience && candidate.workExperience.length) {
      detailsHtml += `<h3 class="mt-3">Work Experience</h3>`;
      candidate.workExperience.forEach(exp => {
        detailsHtml += `
          <div class="mb-2">
            <p><strong>Company:</strong> ${exp.company || ''}</p>
            <p><strong>Title:</strong> ${exp.position || exp.title || ''}</p>
            <p><strong>Duration:</strong> ${exp.employmentDuration || exp.duration || ''}</p>
            <p><strong>Contributions:</strong> ${exp.notableContributions || ''}</p>
          </div>
        `;
      });
    }
    if (candidateDetailsDiv) {
      candidateDetailsDiv.innerHTML = detailsHtml;
    }
    if (candidateModalEl) {
      if (!candidateModalInstance) {
        candidateModalInstance = new bootstrap.Modal(candidateModalEl, {
          keyboard: true
        });
      }
      candidateModalInstance.show();
    }
  };

  window.closeCandidateModal = function() {
    if (candidateModalEl && candidateModalInstance) {
      candidateModalInstance.hide();
    }
  };

  window.checkAll = function() {
    const selectAllCheckbox = document.getElementById('select-all');
    const checkboxes = document.getElementsByName('select_candidate');
    for (let i = 0; i < checkboxes.length; i++) {
      checkboxes[i].checked = selectAllCheckbox.checked;
    }
  };

  // Function to display response data in the frontend
  async function displayResponse(fileName, data) {
    const section = document.createElement('div');
    section.className = 'response-section';

    const candidateProfile = data.candidateProfile;
    const currentLocation = candidateProfile.standardFields.currentLocation
        ? candidateProfile.standardFields.currentLocation.answer
        : 'N/A';

    const workExperience = candidateProfile.standardFields.workExperience
        ? `${JSON.parse(candidateProfile.standardFields.workExperience.answer).Years} years, ${JSON.parse(candidateProfile.standardFields.workExperience.answer).Months} months`
        : 'N/A';

    const educationDetails = candidateProfile.educationDetails
        .map(ed => `${ed.degree} (${ed.branch}) - ${ed.university} (${ed.location})`)
        .join('<br>');

    const experienceDetails = candidateProfile.experienceDetails
        .map(ed => `${ed.designation} at ${ed.companyName} (${ed.location}) from ${ed.dateOfJoining.split('T')[0]} to ${ed.dateOfRelieving.split('T')[0]}`)
        .join(', ');

    const skills = candidateProfile.skills.map(skill => skill.name).join(', ');

    section.innerHTML = `
        <h2>File: ${fileName}</h2>
        <table>
            <tr><th>Full Name</th><td contenteditable="true">${candidateProfile.displayName}</td></tr>
            <tr><th>First Name</th><td contenteditable="true">${candidateProfile.firstName}</td></tr>
            <tr><th>Middle Name</th><td contenteditable="true">${candidateProfile.middleName}</td></tr>
            <tr><th>Last Name</th><td contenteditable="true">${candidateProfile.lastName}</td></tr>
            <tr><th>Email</th><td contenteditable="true">${candidateProfile.email}</td></tr>
            <tr><th>Mobile</th><td contenteditable="true">${candidateProfile.mobilePhone.countryCode}${candidateProfile.mobilePhone.number}</td></tr>
            <tr><th>Current Location</th><td contenteditable="true">${currentLocation}</td></tr>
            <tr><th>Work Experience</th><td contenteditable="true">${workExperience}</td></tr>
            <tr><th>Education Details</th><td contenteditable="true">${educationDetails}</td></tr>
            <tr><th>Experience Details</th><td contenteditable="true">${experienceDetails}</td></tr>
            <tr><th>Skills</th><td contenteditable="true">${skills}</td></tr>
        </table>
    `;
    responseContainer.appendChild(section);
  }
});

