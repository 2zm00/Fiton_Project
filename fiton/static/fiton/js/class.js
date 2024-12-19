document.addEventListener('DOMContentLoaded', function () {
    const center = document.querySelector('#id_center');
    const instructorSelect = document.querySelector('#id_instructor'); // 'instructor' 필드
    const role = userRole;
    
    if (center && instructorSelect) {
        center.addEventListener('change', function () {
            
            if (role === 'centerowner'){
                const selectedCenter = center.value;
                const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

                axios.post('/class/open/choice/', { center: selectedCenter }, {
                    headers: {
                        'X-CSRFToken': csrfToken,
                        'Content-Type': 'application/json',
                    },
                })
                .then(response => {
                    const data = response.data;

                    if (data.instructors) {
                        // 기존 옵션 제거
                        instructorSelect.innerHTML = '<option value="">---------</option>';
                        
                        // 새로운 옵션 추가
                        data.instructors.forEach(function (instructor) {
                            const option = document.createElement('option');
                            option.value = instructor.id;
                            option.textContent = instructor.user__name;
                            instructorSelect.appendChild(option);
                        });
                    } else {
                        alert('관련 강사를 불러오지 못했습니다.');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('오류가 발생했습니다. 다시 시도해주세요.');
                });
            }
        });
    }
    
});
