document.getElementById('review-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const form = this;
    const formData = new FormData(form);
    const classId = form.getAttribute('data-class-id');

    fetch(`/class/${classId}/submit_review/`, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': formData.get('csrfmiddlewaretoken'),
        },
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.errors) {
                alert('폼 오류가 있습니다. 다시 확인해주세요.');
            } else {
                const reviewHTML = `
                    <li>
                        <strong>${data.author}</strong>: ${data.rating}점<br>
                        ${data.comment}<br>
                        작성일: ${data.created_at}
                    </li>
                `;
                document.getElementById('review-list').insertAdjacentHTML('beforeend', reviewHTML);
                form.reset();
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('리뷰를 작성하는 도중 오류가 발생했습니다. 다시 시도해주세요.');
        });
});
